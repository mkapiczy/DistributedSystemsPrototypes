# For tcp connections nodes in between
import zerorpc
# For coroutines
import gevent
# System specific parameters
import sys
# Enums for nodestate
from enum import Enum

class NodeState(Enum):
    NORMAL = 'Normal'
    ELECTION = 'Election'
    REORGANIZATION = 'Reorganization'
    DOWN = 'Down'

class NodeStateVector():
    # PARAMS
    # State: The state of the node
    # Leader: The nodes leader
    # TaskDescription: Description og the task of the node
    # HaltingNode: The node recently makes this node halt
    # NodesUp: Array of other nodes in the system
    def __init__(self):
        self.state = NodeState.NORMAL
        self.leader = 0
        self.taskDescription = None
        self.haltingNode = -1
        self.nodesUp = []

class BullyAlgorithm():
    def __init__(self, addr):
        self.NodeStateVector = NodeStateVector()
        self.NodeStateVector.state = NodeState.NORMAL

        self.check_servers_greenlet = None
        self.myAddress = addr

        # Initialize all servers
        self.servers = []
        self.servers.append("127.0.0.1:9000")
        self.servers.append("127.0.0.1:9001")
        self.servers.append("127.0.0.1:9002")
        self.servers.append("127.0.0.1:9003")
        self.servers.append("127.0.0.1:9004")

        print('My addr: %s' % self.myAddress)
        print('Server list: %s' % (str(self.servers)))

        self.nuberOfNodes = len(self.servers)
        self.connections = []

        # Connect to each other server
        for i, server in enumerate(self.servers):
            if server == self.myAddress:
                self.ownIndex = i
                self.connections.append(self)
            else:
                clientConn = zerorpc.Client(timeout=2)
                clientConn.connect('tcp://' + server)
                self.connections.append(clientConn)

    def askForStatus(self):
        return True

    def isStatusNormal(self):
        return self.NodeStateVector.state == NodeState.NORMAL

    def halt(self, haltingNodeIndex):
        self.NodeStateVector.state = NodeState.ELECTION
        self.NodeStateVector.haltingNode = haltingNodeIndex

    def callNewLeader(self, newLeader):
        print('Calling newLeader')
        if self.NodeStateVector.haltingNode == newLeader and self.NodeStateVector.state == NodeState.ELECTION:
            self.NodeStateVector.leader = newLeader
            self.NodeStateVector.state = NodeState.REORGANIZATION

    def ready(self, j, x=None):
        print('Call ready')
        if self.NodeStateVector.leader == j and self.NodeStateVector.state == NodeState.REORGANIZATION:
            self.NodeStateVector.taskDescription = x
            self.NodeStateVector.state = NodeState.NORMAL

    def callElection(self):
        print('Check the states of higher priority nodes - if there are any higher priority:')
        for i, server in enumerate(self.servers[self.ownIndex + 1:]):
            try:
                self.connections[self.ownIndex + 1 + i].askForStatus()
                if self.check_servers_greenlet is None:
                    self.NodeStateVector.leader = self.ownIndex + 1 + i
                    self.NodeStateVector.state = NodeState.NORMAL
                    self.check_servers_greenlet = self.pool.spawn(self.check())
                return
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % server)

        print('No higher priority nodes - So halt all lower priority nodes including this node:')
        self.halt(self.ownIndex)
        self.NodeStateVector.state = NodeState.ELECTION
        self.NodeStateVector.haltingNode = self.ownIndex
        self.NodeStateVector.nodesUp = []
        for i, server in enumerate(self.servers[self.ownIndex::-1]):
            try:
                self.connections[i].halt(self.ownIndex)
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % server)
                continue
            self.NodeStateVector.nodesUp.append(self.connections[i])

        # Reached the 'election point', inform other nodes about new leader - yourself
        print('Inform nodes of the new leader:')
        self.NodeStateVector.leader = self.ownIndex
        self.NodeStateVector.state = NodeState.REORGANIZATION
        for node in self.NodeStateVector.nodesUp:
            try:
                node.callNewLeader(self.ownIndex)
            except zerorpc.TimeoutExpired:
                print('Timeout! Election will be restarted.')
                self.callElection()
                return

        # Reorganization
        for node in self.NodeStateVector.nodesUp:
            try:
                node.ready(self.ownIndex, self.NodeStateVector.taskDescription)
            except zerorpc.TimeoutExpired:
                print('Timeout!')
                self.callElection()
                return

        self.NodeStateVector.state = NodeState.NORMAL
        print('[%s] Starting ZeroRPC Server' % self.servers[self.ownIndex])
        self.check_servers_greenlet = self.pool.spawn(self.check())

    def recovery(self):
        self.NodeStateVector.haltingNode = -1
        self.callElection()

    def check(self):
        while True:
            gevent.sleep(2)
            if self.NodeStateVector.state == NodeState.NORMAL and self.NodeStateVector.leader == self.ownIndex:
                for i, server in enumerate(self.servers):
                    if i != self.ownIndex:
                        try:
                            response = self.connections[i].isStatusNormal()
                            print('%s : are_you_normal = %s' % (server, response))
                        except zerorpc.TimeoutExpired:
                            print('%s Timeout!' % server)
                            continue

                        if not response:
                            self.callElection()
                            return
            elif self.NodeStateVector.state == NodeState.NORMAL and self.NodeStateVector.leader != self.ownIndex:
                print('Check leader\'s state')
                try:
                    result = self.connections[self.NodeStateVector.leader].askForStatus()
                    print('%s : are_you_there = %s' % (self.servers[self.NodeStateVector.leader], result))
                except zerorpc.TimeoutExpired:
                    print('Leader down, Carry out new eleciton.')
                    self.timeout()

    def timeout(self):
        if self.NodeStateVector.state == NodeState.NORMAL or self.NodeStateVector.state == NodeState.REORGANIZATION:
            try:
                self.connections[self.NodeStateVector.leader].askForStatus()
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % self.servers[self.NodeStateVector.leader])
                self.callElection()
        else:
            self.callElection()

    def start(self):
        self.pool = gevent.pool.Group()
        self.recovery_greenlet = self.pool.spawn(self.recovery)


def main():
    ownAddress = sys.argv[1]
    bully = BullyAlgorithm(ownAddress)
    s = zerorpc.Server(bully)
    s.bind('tcp://' + ownAddress)
    bully.start()
    # Start server
    print('[%s] Starting ZeroRPC Server' % ownAddress)
    s.run()

if __name__ == '__main__':
    main()