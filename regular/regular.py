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

def simulate(ndfsm):
    return

def json_to_ndfsm(json_fsm):
    return


#
#
#
#
#
#
#
#
#
#
#
#

def ndfsm_to_dfsm(ndfsm):
    dfsm = {}
    dfsm['alphabet'] = ndfsm['alphabet']

    #compute eps of each state in ndfsm
    epsilons = {}
    for q in range(ndfsm['states']):
        epsilons[q] = eps(q, ndfsm['trans'])

    start = epsilons[0]
    active_states = set()
    active_states.add(frozenset(start))

    # set of states for which transitions have been computed
    unvisited = set()
    unvisited.add(frozenset(start))
    visited = set()

    # all the ndfsm relations
    trans = ndfsm['trans']
    new_trans = {}
    i = 0;
    while unvisited:
        Q = unvisited.pop()
        visited.add(Q)
        # for every alphabet symbol
        for c in ndfsm['alphabet']:
            new_state = set()
            # for all states q in Q
            for q in Q:
                # if transition (q, c, p) exists, update new_state
                # with eps(p, trans)
                if (q, c) in trans:
                    p = trans[(q, c)]
                    for x in p:
                        new_state.update(eps(x, trans))
            new_trans[(Q, c)] = new_state
            active_states.add(frozenset(new_state))
            if not new_state in visited:
                unvisited.add(frozenset(new_state))

    # enumerate each new state and substitute
    enum = {frozenset(start):0}
    i = 1
    accept = set()
    for state in active_states:
        if state == frozenset(start):
            continue
        enum[state] = i
        if state.intersection(ndfsm['accept']):
            accept.add(state)
        i += 1
    #print("enum: " + str(enum))
    #print("accept: " + str(accept))

    accept_final = set()
    for state in accept:
        accept_final.add(enum[state])

    trans_final = {}
    for t in new_trans:
        trans_final[(enum[t[0]], t[1])] = set([enum[frozenset(new_trans[t])]])

    m = {'alphabet':ndfsm['alphabet'], 'states':len(active_states), 'trans':trans_final, 'accept':accept_final}
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
    return result

def reduce(dfsm):
    return

if __name__ == "__main__":
    m = {}
    alpha = set()
    alpha.add('a');
    alpha.add('b');
    m['alphabet'] = alpha
    m['states'] = 6
    trans = {}
    trans[(0, 'a')] = set([0])
    trans[(0, 'b')] = set([0])
    trans[(0, '')] = set([1])
    trans[(1, 'a')] = set([2])
    trans[(2, 'a')] = set([3])
    trans[(3, 'b')] = set([4])
    trans[(4, 'a')] = set([5])
    m['trans'] = trans
    m['accept'] = set([5])
    print(ndfsm_to_dfsm(m))


