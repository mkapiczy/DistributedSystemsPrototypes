import zerorpc
import gevent
import sys

# How to run the program?
# Run nodes separately e.g.
# python bully.py 127.0.0.1:9000
# python bully.py 127.0.0.1:9001
# python bully.py 127.0.0.1:9002
# python bully.py 127.0.0.1:9003
# python bully.py 127.0.0.1:9004
# Node on port 9004 will be the leader. Killing a node will force new election, which will result in node 9003 to be chosen as a new leader.

class StateVector():
    def __init__(self):
        # state of the node
        # [Down, Election, Reorganization, Normal]
        self.state = 'Normal'
        # leader of the node
        self.leader = 0
        # description of task
        self.taskDescription = None
        # the node recently makes this node halt
        self.haltingNode = -1
        # list of nodes which this node believes to be in operation
        self.nodesUp = []


class Bully():
    def __init__(self, addr, config_file='config'):
        self.StateVector = StateVector()
        self.StateVector.state = 'Normal'

        self.check_servers_greenlet = None

        self.myAddress = addr

        self.servers = []
        f = open(config_file, 'r')
        for line in f.readlines():
            line = line.rstrip()
            self.servers.append(line)
        print('My addr: %s' % self.myAddress)
        print('Server list: %s' % (str(self.servers)))

        self.nuberOfNodes = len(self.servers)

        self.connections = []

        for i, server in enumerate(self.servers):
            if server == self.myAddress:
                self.ownIndex = i
                self.connections.append(self)
            else:
                c = zerorpc.Client(timeout=2)
                c.connect('tcp://' + server)
                self.connections.append(c)

    def areYouThere(self):
        return True

    def areYouNormal(self):
        return self.StateVector.state == 'Normal'

    def halt(self, haltingNodeIndex):
        self.StateVector.state = 'Election'
        self.StateVector.haltingNode = haltingNodeIndex

    def newLeader(self, newLeader):
        print('Call newLeader')
        if self.StateVector.haltingNode == newLeader and self.StateVector.state == 'Election':
            self.StateVector.leader = newLeader
            self.StateVector.state = 'Reorganization'

    def ready(self, j, x=None):
        print('Call ready')
        if self.StateVector.leader == j and self.StateVector.state == "Reorganization":
            self.StateVector.taskDescription = x
            self.StateVector.state = 'Normal'

    def election(self):
        print('Check the states of higher priority nodes - if there are any higher priority:')
        for i, server in enumerate(self.servers[self.ownIndex + 1:]):
            try:
                self.connections[self.ownIndex + 1 + i].areYouThere()
                if self.check_servers_greenlet is None:
                    self.StateVector.leader = self.ownIndex + 1 + i
                    self.StateVector.state = 'Normal'
                    self.check_servers_greenlet = self.pool.spawn(self.check())
                return
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % server)

        print('No higher priority nodes - So halt all lower priority nodes including this node:')
        self.halt(self.ownIndex)
        self.StateVector.state = 'Election'
        self.StateVector.haltingNode = self.ownIndex
        self.StateVector.nodesUp = []
        for i, server in enumerate(self.servers[self.ownIndex::-1]):
            try:
                self.connections[i].halt(self.ownIndex)
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % server)
                continue
            self.StateVector.nodesUp.append(self.connections[i])

        # Reached the 'election point', inform other nodes about new leader - yourself
        print('Inform nodes of the new leader:')
        self.StateVector.leader = self.ownIndex
        self.StateVector.state = 'Reorganization'
        for node in self.StateVector.nodesUp:
            try:
                node.newLeader(self.ownIndex)
            except zerorpc.TimeoutExpired:
                print('Timeout! Election will be restarted.')
                self.election()
                return

        # Reorganization
        for node in self.StateVector.nodesUp:
            try:
                node.ready(self.ownIndex, self.StateVector.taskDescription)
            except zerorpc.TimeoutExpired:
                print('Timeout!')
                self.election()
                return

        self.StateVector.state = 'Normal'
        print('[%s] Starting ZeroRPC Server' % self.servers[self.ownIndex])
        self.check_servers_greenlet = self.pool.spawn(self.check())

    def recovery(self):
        self.StateVector.haltingNode = -1
        self.election()

    def check(self):
        while True:
            gevent.sleep(2)
            if self.StateVector.state == 'Normal' and self.StateVector.leader == self.ownIndex:
                for i, server in enumerate(self.servers):
                    if i != self.ownIndex:
                        try:
                            response = self.connections[i].areYouNormal()
                            print('%s : are_you_normal = %s' % (server, response))
                        except zerorpc.TimeoutExpired:
                            print('%s Timeout!' % server)
                            continue

                        if not response:
                            self.election()
                            return
            elif self.StateVector.state == 'Normal' and self.StateVector.leader != self.ownIndex:
                print('Check leader\'s state')
                try:
                    result = self.connections[self.StateVector.leader].areYouThere()
                    print('%s : are_you_there = %s' % (self.servers[self.StateVector.leader], result))
                except zerorpc.TimeoutExpired:
                    print('Leader down, Carry out new eleciton.')
                    self.timeout()

    def timeout(self):
        if self.StateVector.state == 'Normal' or self.StateVector.state == 'Reorganization':
            try:
                self.connections[self.StateVector.leader].areYouThere()
            except zerorpc.TimeoutExpired:
                print('%s Timeout!' % self.servers[self.StateVector.leader])
                self.election()
        else:
            self.election()

    def start(self):
        self.pool = gevent.pool.Group()
        self.recovery_greenlet = self.pool.spawn(self.recovery)


def main():
    addr = sys.argv[1]
    bully = Bully(addr)
    s = zerorpc.Server(bully)
    s.bind('tcp://' + addr)
    bully.start()
    # Start server
    print('[%s] Starting ZeroRPC Server' % addr)
    s.run()


if __name__ == '__main__':
    main()