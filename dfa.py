
# https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
# Deterministic Finite Automata representation

dfa = {0:{'0':0, '1':1},
      1:{'0':2, '1':0},
      2:{'0':1, '1':2}}

# Running dfa against an input string drawn from the alphabet in question 
# (after specifying the initial state and the set of accepting values) is then straightforward.
def accepts(transitions,initial,accepting,s):
  state = initial
  for c in s:
      state = transitions[state][c]
  return state in accepting

# We start in the initial state, step through the string character by character, and at each step simply look up the next state. 
# When we are done stepping through the string we simply check if the final state is in the set of accepting states.
print("1011101")
print(accepts(dfa,0,{0},'1011101'))
# E.g. accepts(dfa,0,{0},'1011101') returns true
print('10111011')
print(accepts(dfa,0,{0},'10111011'))
# While accepts(dfa,0,{0},'10111011') returns false