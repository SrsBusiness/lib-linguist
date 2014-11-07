#!/usr/bin/python

import copy

# grammars are a set of tuples (X, Y) where X is a nonterminal and Y is 
# in the kleene star of terminals and nonterminals. Nonterminals are denoted
# as integers starting at 0, which is implicitly the starting nonterminal.
# A context-free grammar is a tuple of the alphabet, the number of
# non-terminals, and the grammar
# E.g.: ({'a', 'b'}, 1, {(0, ('a', 0,'b')), (0, (''))})

ALPHABET = 0
NONTERMINALS = 1
GRAMMAR = 2

def remove_unproductive(cfg):
    unproductive = {x for x in range(cfg[NONTERMINALS])}
    old_size = len(unproductive)
    while True:
        for rule in cfg[GRAMMAR]:
            if rule[0] not in unproductive:
                continue
            if rhs_not_in(rule[1], unproductive):
                unproductive.remove(rule[0])
        if old_size == len(unproductive):
            break;
        old_size = len(unproductive)

    # re-enumerate nonterminals
    i = cfg[NONTERMINALS] - len(unproductive) - 1
    non_terminal_new = i + 1
    new_map = {0:0}
    for x in range(cfg[NONTERMINALS]):
        if x == 0:
            continue
        elif x not in unproductive:
            new_map[x] = i
            i -= 1

    new_grammar = set()
    for rule in cfg[GRAMMAR]:
        if rule[0] not in unproductive and \
                rhs_not_in(rule[1], unproductive):
            # create new rule
            lhs = new_map[rule[0]]
            rhs = []
            for char in rule[1]:
                if char in new_map:
                    rhs.append(new_map[char])
                else:
                    rhs.append(char)
            new_grammar.add((lhs, tuple(rhs)))
    return (cfg[ALPHABET], non_terminal_new, new_grammar)

def rhs_not_in(rhs, unproductive):
    all_productive = True
    for char in rhs:
        all_productive = all_productive and char not in unproductive
        if not all_productive:
            break
    return all_productive

def rhs_in(rhs, unproductive):
    all_productive = True
    for char in rhs:
        all_productive = all_productive and char in unproductive
        if not all_productive:
            break
    return all_productive

def remove_unreachable(cfg):
    unreachable = {x for x in range(1, cfg[NONTERMINALS])}
    old_size = len(unreachable)
    while True:
        for rule in cfg[GRAMMAR]:
            if rule[0] not in unreachable:
                for element in rule[1]:
                    if element in unreachable:
                        unreachable.remove(element)
        if old_size == len(unreachable):
            break
        old_size = len(unreachable)

    # re-enumerate nonterminals
    enum = {0:0}
    i = cfg[NONTERMINALS] - len(unreachable) - 1
    non_terminal_new = i + 1
    for x in range(cfg[NONTERMINALS]):
        if x == 0:
            continue
        if x not in unreachable:
            enum[x] = i
            i -= 1
    # create new grammar
    new_grammar = set()
    for rule in cfg[GRAMMAR]:
        if rule[0] not in unreachable:
            lhs = enum[rule[0]]
            rhs = []
            for char in rule[1]:
                if char in enum:
                    rhs.append(enum[char])
                else:
                    rhs.append(char)
            new_grammar.add((lhs, tuple(rhs)))
    return (cfg[ALPHABET], non_terminal_new, new_grammar)

def remove_eps(cfg):
    #nullable = {x for x in range(cfg[NONTERMINALS])}
    nullable = set()
    new_grammar = copy.deepcopy(cfg[GRAMMAR])
    for rule in cfg[GRAMMAR]:
        if rule[1] == ('',):
            nullable.add(rule[0])
            new_grammar.remove(rule)
    old_size = len(nullable)
    while True:
        for rule in cfg[GRAMMAR]:
            if rule[0] not in nullable and rhs_in(rule[1], nullable):
                nullable.add(rule[0])
        if old_size == len(nullable):
            break
        old_size = len(nullable)
    print(new_grammar)
    print()
    contains_eps = 0 in nullable
    old_size = len(new_grammar)
    while True:
        for rule in list(new_grammar):
            if len(rule[1]) > 1:
                for char in rule[1]:
                    if char in nullable:
                        #print(rule)
                        #print((rule[0], tuple([x for x in rule[1]\
                        #    if x != char])))
                        #print()
                        new_grammar.add((rule[0], tuple([x for x in rule[1]\
                            if x != char])))
        if old_size == len(new_grammar):
            break
        old_size = len(new_grammar)
    print(new_grammar)
    print()

    

    if contains_eps:
        nonterminals = cfg[NONTERMINALS] + 1
        old_grammar = new_grammar
        new_grammar = set()
        for rule in old_grammar:
            lhs = nonterminals - 1 if rule[0] == 0 else rule[0]
            rhs = []
            for char in rule[1]:
                rhs.append(char if char != 0 else nonterminals - 1)
            new_grammar.add((lhs, tuple(rhs)))
        new_grammar.add((0, ('',)))
        new_grammar.add((0, (nonterminals - 1,)))

    print(new_grammar)
    print()


def top_down_parse(cfg):
    return

if __name__ == "__main__":
    #cfg = ({'a', 'b'}, 5, {
    #    (0, (1, 2)),
    #    (0, (1, 3)),
    #    (1, ('a', 1, 'b')),
    #    (1, ('',)),
    #    (2, ('',)),
    #    (2, ('b', 1)),
    #    (3, ('b', 3, 'a')),
    #    (4, (1,))
    #    })
    cfg = ({'(', ')'}, 1, {
        (0, ('(', 0, ')')),
        (0, (0, 0)),
        (0, ('',)),
        })

    #print(remove_unproductive(cfg))
    #print()
    #print(remove_unreachable(cfg))
    #print()
    #print(remove_unproductive(remove_unreachable(cfg)))
    remove_eps(cfg)
