# This dfsm has thirty one states and can
# likely be reduced to seven states.
minimize_test = (
    31,
    {'0', '1'},
    {
        (0, '0'): {1},
        (0, '1'): {2},
        (1, '0'): {3},
        (1, '1'): {4},
        (2, '0'): {5},
        (2, '1'): {6},
        (3, '0'): {7},
        (3, '1'): {8},
        (4, '0'): {9},
        (4, '1'): {10},
        (5, '0'): {11},
        (5, '1'): {12},
        (6, '0'): {13},
        (6, '1'): {14},
        (7, '0'): {15},
        (7, '1'): {16},
        (8, '0'): {17},
        (8, '1'): {18},
        (9, '0'): {19},
        (9, '1'): {20},
        (10, '0'): {21},
        (10, '1'): {22},
        (11, '0'): {23},
        (11, '1'): {24},
        (12, '0'): {25},
        (12, '1'): {26},
        (13, '0'): {27},
        (13, '1'): {28},
        (14, '0'): {29},
        (14, '1'): {30},
        (15, '0'): {0},
        (15, '1'): {0},
        (16, '0'): {0},
        (16, '1'): {0},
        (17, '0'): {0},
        (17, '1'): {0},
        (18, '0'): {0},
        (18, '1'): {0},
        (19, '0'): {0},
        (19, '1'): {0},
        (20, '0'): {0},
        (20, '1'): {0},
        (21, '0'): {0},
        (21, '1'): {0},
        (22, '0'): {0},
        (22, '1'): {0},
        (23, '0'): {0},
        (23, '1'): {0},
        (24, '0'): {0},
        (24, '1'): {0},
        (25, '0'): {0},
        (25, '1'): {0},
        (26, '0'): {0},
        (26, '1'): {0},
        (27, '0'): {0},
        (27, '1'): {0},
        (28, '0'): {0},
        (28, '1'): {0},
        (29, '0'): {0},
        (29, '1'): {0},
        (30, '0'): {0},
        (30, '1'): {0},
    },
    {20, 24}
)