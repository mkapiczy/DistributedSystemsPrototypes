processesWrong = {'P1': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6},
                  'P2': {'g': 1, 'h': 2, 'i': 3},
                  'P3': {'j': 1, 'k': 2}}

processesCorrect = {'P1': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6},
                    'P2': {'g': 1, 'h': 2, 'i': 3},
                    'P3': {'j': 1, 'k': 2}}

messages = {'j': 'c', 'g': 'd', 'e': 'h', 'f': 'k'}


def correctOrderingAccordingToLamportRules():
    for key, value in messages.items():
        senderClock = None
        receiverClock = None

        for p in processesWrong:

            i = 0
            while senderClock is None and i < len(processesWrong[p]) - 1:
                senderClock = processesWrong[p].get(key)
                i += 1

            i = 0
            while receiverClock is None and i < len(processesWrong[p]) - 1:
                receiverClock = processesWrong[p].get(value)
                i += 1

        if receiverClock <= senderClock:
            for p in processesWrong:
                if processesWrong[p].get(value) is not None:
                    processesCorrect[p][value] = senderClock + 1

    for p in processesCorrect:
        previousValue = list(processesCorrect[p].values())[0] - 1
        for key, value in processesCorrect[p].items():
            if (value <= previousValue):
                processesCorrect[p][key] = previousValue + 1
            previousValue = value


print('Processes wrong ordering ' + str(processesWrong))

correctOrderingAccordingToLamportRules()

print('Processes correct ordering ' + str(processesCorrect))