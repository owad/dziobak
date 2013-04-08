# -* - coding: utf-8 -*-


### GLOBAL VARS ###

# Statuses
REG = 1000
NEW = 2000
PROG = 3000
TO_APPR = 4000
APPR = 5000
TO_EXT = 6000
AT_EXT = 7000
FROM_EXT = 8000
READY = 9000
CLOSED = 10000

STATUSES = [
    (REG, 'zarejestrowane'),
    (NEW, 'przyjęte'),
    (PROG, 'w realizacji'),
    (TO_APPR, 'do akceptacji'),
    (APPR, 'zakaceptowane'),    
    (TO_EXT, 'do wysłania'),
    (AT_EXT, 'w serwisie zewnętrznym'),
    (FROM_EXT, 'odebrane z serwisu zewnętrznego'),
    (READY, 'do wydania'),
    (CLOSED, 'wydane'),

]

STATUS_NAMES = dict(STATUSES)

### OUT DATED SETS

# 3 DAYS
OUT_OF_DATE_3 = (REG, NEW, PROG, TO_APPR, APPR, TO_EXT)

# 7 DAYS
OUT_OF_DATE_7 = (FROM_EXT, READY)

# 10 DAYS 
OUT_OF_DATE_10 = (AT_EXT,)


### Custom statuses flow for normal clients ###

C1_STATUSES = [
    (NEW, STATUS_NAMES[NEW]),
    (PROG, STATUS_NAMES[PROG]),
    (TO_EXT, STATUS_NAMES[TO_EXT]),
    (AT_EXT, STATUS_NAMES[AT_EXT]),
    (FROM_EXT, STATUS_NAMES[FROM_EXT]),
    (READY, STATUS_NAMES[READY]),
    (CLOSED, STATUS_NAMES[CLOSED]),

]

C1_STATUS_NAMES = dict(C1_STATUSES)

C1_STATUSES_FLOW = {
    NEW: [PROG],
    PROG: [TO_EXT, READY],
    TO_EXT: [AT_EXT],
    AT_EXT: [FROM_EXT],
    FROM_EXT: [PROG, READY],
    READY: [CLOSED],
    CLOSED: []
}


### Custom status flow for client with access ###

C2_STATUSES = [
    (REG, STATUS_NAMES[REG]),
    (NEW, STATUS_NAMES[NEW]),
    (PROG, STATUS_NAMES[PROG]),
    (TO_APPR, STATUS_NAMES[TO_APPR]),
    (APPR, STATUS_NAMES[APPR]),    
    (READY, STATUS_NAMES[READY]),
    (CLOSED, STATUS_NAMES[CLOSED]),
]

C2_STATUS_NAMES = dict(C2_STATUSES)

C2_STATUSES_FLOW = {
    REG: [NEW],
    NEW: [PROG],
    PROG: [TO_APPR],
    TO_APPR: [APPR],
    APPR: [READY],
    READY: [CLOSED],
    CLOSED: []
}

def get_status_flow(product):
    if product.user.is_client:
        return C1_STATUS_FLOW
    if product.user.is_client_with_access:
        return C2_STATUS_FLOW

