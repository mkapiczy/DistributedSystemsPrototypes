processesWrong = {'P1': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
                  'P2': {'e': 1, 'f': 2, 'g': 3},
                  'P3': {'h': 1, 'i': 2}}

processesCorrect = {'P1': {'a': 1, 'b': 2, 'c': 3, 'd': 4},
                    'P2': {'e': 1, 'f': 2, 'g': 3},
                    'P3': {'h': 1, 'i': 2}}

messages = {'h': 'b', 'c': 'f', 'd': 'i'}

def correctReceiverClock(receiveOperation, senderClock):
    for p in processesWrong:
        if processesWrong[p].get(receiveOperation) is not None:
            processesCorrect[p][receiveOperation] = senderClock + 1


def correctLocalOrdering(process):
    previousValue = list(processesCorrect[process].values())[0] - 1
    for key, value in processesCorrect[process].items():
        if value <= previousValue:
            processesCorrect[process][key] = previousValue + 1
        previousValue = value


def correctOrderingAccordingToLamportRules():
    # iterate through messages in the system
    for sendOperation, receiveOperation in messages.items():
        senderClock = None
        receiverClock = None

        # iterate through processes
        for process in processesWrong:
            i = 0
            while senderClock is None and i < len(processesWrong[process]) - 1:
                senderClock = processesWrong[process].get(sendOperation)
                i += 1

            i = 0
            while receiverClock is None and i < len(processesWrong[process]) - 1:
                receiverClock = processesWrong[process].get(receiveOperation)
                i += 1

        if receiverClock <= senderClock:
            correctReceiverClock(receiveOperation, senderClock)

    for p in processesCorrect:
        correctLocalOrdering(p)


print('Processes wrong ordering ' + str(processesWrong))

correctOrderingAccordingToLamportRules()

print('Processes correct ordering ' + str(processesCorrect))
