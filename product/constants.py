# -* - coding: utf-8 -*-

# Statuses
NEW = 10
PROG = 20
TO_EXT = 30
AT_EXT = 40
FROM_EXT = 50
READY = 60
CLOSED = 70

STATUSES = [
    (NEW, 'przyjęty'),
    (PROG, 'w realizacji'),
    (TO_EXT, 'do wysłania'),
#    (AT_EXT, 'w serwisie zewnętrznym'),
#    (FROM_EXT, 'odebrano z serwisu zewnętrznego'),
#    (READY, 'do wydania'),
    (CLOSED, 'wydany')]

STATUS_NAMES = dict(STATUSES)

# Custom statuses flow

# Admins
STATUSES_FLOW = {
    NEW: [PROG],
    PROG: [TO_EXT, READY],
    TO_EXT: [AT_EXT],
    AT_EXT: [FROM_EXT],
    FROM_EXT: [PROG, READY],
    READY: [CLOSED]
}

