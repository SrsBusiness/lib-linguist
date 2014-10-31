#!/usr/bin/python

from json import *

# { "alphabet"  :   Set(['a', b', 'c']),
#   "states"    :   5,
#   "trans"     :   {   
#                       (0, 'c')    :   [0, 1]
#                       ...
#                   },
#   "accept"    :   Set([2, 3])
# }

STATES = 0
ALPHABET = 1
TRANS = 2
ACCEPT = 3

def simulate(ndfsm):
    return

def json_to_ndfsm(json_fsm):
    return

def ndfsm_to_dfsm(ndfsm):
    #compute eps of each state in ndfsm
    epsilons = {}
    for q in range(ndfsm[STATES]):
        epsilons[q] = eps(q, ndfsm[TRANS])

    start = epsilons[0]
    active_states = set()
    active_states.add(0)

    # set of states for which transitions have been computed
    unvisited = set()
    unvisited.add(start)
    visited = set()

    # all the ndfsm relations
    trans = ndfsm[TRANS]
    new_trans = {}
    enum = {start:0}
    num_states = 1
    accept = set()
    if start.intersection(ndfsm[ACCEPT]):
        accept.add(enum[start])
    while unvisited:
        Q = unvisited.pop()
        visited.add(Q)
        # for every alphabet symbol
        for c in ndfsm[ALPHABET]:
            new_state = set()
            # for all states q in Q
            for q in Q:
                # if transition (q, c, p) exists, update new_state
                # with eps(p, trans)
                if (q, c) in trans:
                    p = trans[(q, c)]
                    for x in p:
                        new_state.update(eps(x, trans))
            new_state_final = frozenset(new_state)
            # if new_state is unvisited, add it to unvisited
            if new_state not in visited:
                unvisited.add(new_state_final)
            # add new_state to enumeration if it isn't already enumerated
            # add it to accept if it contains an accepting state from ndfsm
            if new_state_final not in enum:
                enum[new_state_final] = num_states
                active_states.add(enum[new_state_final])
                if new_state_final.intersection(ndfsm[ACCEPT]):
                    accept.add(enum[new_state_final])
                num_states += 1
            # add transition
            new_trans[(enum[Q], c)] = {enum[new_state_final]}

    m = (num_states, ndfsm[ALPHABET], new_trans, accept)
    return m

def eps(q, trans):
    result = set()
    unvisited = set()
    visited = set()
    result.add(q)
    unvisited.add(q)
    i = 0
    while unvisited and i < 20:
        i += 1
        p = unvisited.pop()
        visited.add(p)
        if (p, '') in trans:
            r = trans[(p, '')]
            result.update(r)
            unvisited.update([x for x in r if not x in visited])
    return frozenset(result)

def reduce(dfsm):
    return

if __name__ == "__main__":
    m = (9, {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}, {
        (0, '') : {1, 2, 3, 4, 5, 6, 7, 8},
        (1, 'b') : {1},
        (1, 'c') : {1},
        (1, 'd') : {1},
        (1, 'e') : {1},
        (1, 'f') : {1},
        (1, 'g') : {1},
        (1, 'h') : {1},
        (2, 'a') : {2},
        (2, 'c') : {2},
        (2, 'd') : {2},
        (2, 'e') : {2},
        (2, 'f') : {2},
        (2, 'g') : {2},
        (2, 'h') : {2},
        (3, 'a') : {3},
        (3, 'b') : {3},
        (3, 'd') : {3},
        (3, 'e') : {3},
        (3, 'f') : {3},
        (3, 'g') : {3},
        (3, 'h') : {3},
        (4, 'a') : {4},
        (4, 'b') : {4},
        (4, 'c') : {4},
        (4, 'e') : {4},
        (4, 'f') : {4},
        (4, 'g') : {4},
        (4, 'h') : {4},
        (5, 'a') : {5},
        (5, 'b') : {5},
        (5, 'c') : {5},
        (5, 'd') : {5},
        (5, 'f') : {5},
        (5, 'g') : {5},
        (5, 'h') : {5},
        (6, 'a') : {6},
        (6, 'b') : {6},
        (6, 'c') : {6},
        (6, 'd') : {6},
        (6, 'e') : {6},
        (6, 'g') : {6},
        (6, 'h') : {6},
        (7, 'a') : {7},
        (7, 'b') : {7},
        (7, 'c') : {7},
        (7, 'd') : {7},
        (7, 'e') : {7},
        (7, 'f') : {7},
        (7, 'h') : {7},
        (8, 'a') : {8},
        (8, 'b') : {8},
        (8, 'c') : {8},
        (8, 'd') : {8},
        (8, 'e') : {8},
        (8, 'f') : {8},
        (8, 'g') : {8},
        }, {0, 1, 2, 3, 4, 5, 6, 7, 8})
    print('NDFSM')
    print(m)
    print()
    print('DFSM')
    print(ndfsm_to_dfsm(m))


