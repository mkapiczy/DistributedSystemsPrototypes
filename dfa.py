
# https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
# Deterministic Finite Automata representation
from timeit import default_timer as timer

dfa = { 0:{'0':0, '1':1},
        1:{'0':2, '1':0},
        2:{'0':1, '1':2}}

# Running dfa against an input string drawn from the alphabet in question 
# (after specifying the initial state and the set of accepting values) is then straightforward.
def accepts(transitions, initial, accepting, s, lastTransitionTimeConstraint):
    state = initial
    start = 0
    end = 0
    for i, c in enumerate(s):
        if isLastTransition(i, s):
            start = timer()
        state = transitions[state][c]
        if isLastTransition(i, s):
            end = timer()
    accept = ((end-start) < lastTransitionTimeConstraint) and state in accepting
    return accept

def isLastTransition(iterator, s):
    return iterator == (len(s)-1)

# We start in the initial state, step through the string character by character, and at each step simply look up the next state. 
# When we are done stepping through the string we simply check if the final state is in the set of accepting states.
print("1011101" + " Last iteration time constraint 1s")
print(accepts(dfa,0,{0},'1011101', 1))
# E.g. accepts(dfa,0,{0},'1011101') returns true
print('10111011' + ' Last iteration time constraint 1s')
print(accepts(dfa,0,{0},'10111011', 1))
# While accepts(dfa,0,{0},'10111011') returns false
print('101101' + " Last iteration time constraint 9.53674316406e-24s")
print(accepts(dfa,0,{0},'1011101', 9.53674316406e-24))
# E.g. accepts(dfa,0,{0},'1011101') returns false because of time constaint