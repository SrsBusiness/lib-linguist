#!/usr/bin/python

from json import *
from test import *

STATES = 0
ALPHABET = 1
TRANS = 2
ACCEPT = 3

def simulate(dfsm, stream):
    state = 0
    for x in stream:
        query = (state, x)
        if query in dfsm[TRANS]:
            # FIXME: dfsm should be represented differently
            result = dfsm[TRANS][query]
            if result: state = list(result)[0]
        else:
            return False
    return state in dfsm[ACCEPT]

def json_to_ndfsm(json_fsm):
    return

# regular expressions are a context free grammar, so this will be postponed
# until CFG parsing is implemented
def regex_to_dfsm(regex):

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

def minimize(dfsm):
    states = dfsm[STATES]
    state_to_class = {}
    accept = frozenset(dfsm[ACCEPT])
    non_accept = frozenset([x for x in range(states) if x not in
        dfsm[ACCEPT]])
    classes = {accept, non_accept}

    # map old states to equivalence classes
    for state in range(states):
        if state in accept:
            state_to_class[frozenset({state})] = accept
        else:
            state_to_class[frozenset({state})] = non_accept

    oldsize = len(classes)
    trans = dfsm[TRANS]
    while classes:
        newclasses = {}
        for Q in classes:
            newclasses[Q] = dict()
            for q in Q:
                next_states = set()
                for c in dfsm[ALPHABET]:
                    p = trans[(q, c)]
                    # map char with equivalence class
                    next_states.add((c, state_to_class[frozenset(p)]))
                next_states_froze = frozenset(next_states)
                if next_states_froze not in newclasses[Q]:
                    newclasses[Q][next_states_froze] = {q}
                else:
                    newclasses[Q][next_states_froze].add(q)
        # newclasses now maps equivalence classes to q
        # each equivalence class is a set of states
        # and each q is a set of states

        # create new set of equivalence classes
        classes = set()
        for e in newclasses:
            for f in newclasses[e]:
                classes.add(frozenset(newclasses[e][f]))

        # remap states to equivalence classes
        state_to_class = {}
        for e in classes:
            for q in e:
                state_to_class[frozenset({q})] = e

        if oldsize == len(classes):
            break
        oldsize = len(classes)

    # enumerate classes
    enum = {}
    size = len(classes)
    i = size - 1
    for e in classes:
        if 0 in e:
            enum[e] = 0
        else:
            enum[e] = i
            i -= 1
    # compute new transitions
    new_trans = {}
    for e in classes:
        for c in dfsm[ALPHABET]:
            for q in e:
                if (q, c) in trans:
                    new_trans[(enum[e], c)] =\
                    {enum[state_to_class[frozenset(trans[(q, c)])]]}
                    break;
    new_accept = set()
    for e in classes:
        if e.intersection(accept):
            new_accept.add(enum[e])
    return (size, dfsm[ALPHABET], new_trans, new_accept)

def equivalence_slow(fsm1, fsm2):
    if fsm1[ALPHABET] != fsm2[ALPHABET]:
        return false
    maxstates = max(fsm1[STATES], fsm2[STATES])
    for i in range(maxstates):
        if not equivalence_slow_recurse(fsm1, fsm2, '', i + 1):
            return false
        print("Passed for all strings of length " + str(i))
    return true

def equivalence_slow_recurse(fsm1, fsm2, inputstr, level):
    if level <= 0:
        return simulate(fsm1, inputstr) == simulate(fsm2, inputstr)
    for c in fsm1[ALPHABET]:
        if not equivalence_slow_recurse(fsm1, fsm2, inputstr + c, level - 1):
            return False
    return True


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
    minfsm = minimize(ndfsm_to_dfsm(m))
    while True:
        print(simulate(minfsm, input()))
    #print('NDFSM')
    #print(m)
    #print()
    #print('DFSM')
    #print(ndfsm_to_dfsm(m))
    #minimize(ndfsm_to_dfsm(m))
    #m = (3, {'a', 'b'}, {(0, 'a'):{1}, (0, 'b'):{1}, (1, 'a'):{2},
    #    (1, 'b'):{2}, (2, 'a'):{1}, (2, 'b'):{1}}, {0, 2})
    #n = (4, {'a', 'b'}, {(0, 'a'):{1}, (0, 'b'):{2}, (1, 'a'):{3},
    #    (1, 'b'):{3}, (2, 'a'):{1}, (2, 'b'):{2}, (3, 'a'):{3}, (3, 'b'):{3}},
    #    {1, 3})
    #minimize(m)
    #a = minimize(minimize_test)
    #print(a)
    #equivalence_slow(a, minimize_test)


