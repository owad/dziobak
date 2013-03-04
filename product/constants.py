# -* - coding: utf-8 -*-
DECIMAL_ZERO = '0.00'

NEW = 10  # przyjety
PROCESSING = 20  # w_realizacji
COURIER = 30  # do_wyslania
EXTERNAL = 40  # w_serwisie
BACK = 50  # z_serwisu
READY = 60  # do_wydania
CLOSED = 70  # wydany

STATUSES = (NEW, PROCESSING, COURIER, EXTERNAL, BACK, READY, CLOSED)

NEW_NICE = 'przyjęty'
PROCESSING_NICE = 'w realizacji'
COURIER_NICE = 'do wysłania'
EXTERNAL_NICE = 'w serwisie zew.'
BACK_NICE = 'odebrano z serwisu zew'
READY_NICE = 'do wydania'
CLOSED_NICE = 'wydany'

STATUS_CHOICES = (
    (NEW, NEW_NICE),
    (PROCESSING, PROCESSING_NICE),
    (COURIER, COURIER_NICE),
    (EXTERNAL, EXTERNAL_NICE),
    (BACK, BACK_NICE),
    (READY, READY_NICE),
    (CLOSED, CLOSED_NICE)
)

IN_PROGRESS = (PROCESSING, COURIER, EXTERNAL, BACK, READY)

FIRST_STATUS = NEW
LAST_STATUS = CLOSED

Y, N = ('Y', 'N')
Y_NICE, N_NICE = ('Tak', 'Nie')
WARRANTY_CHOICES = ( 
    (N, N_NICE),
    (Y, Y_NICE)
)


COMMENT, STATUS_CHANGE, HARDWARE_ADD = ('komentarz', 'zmiana_statusu', 'sprzet')
COMMENT_NICE, STATUS_CHANGE_NICE, HARDWARE_ADD_NICE = ('komenatrz', 'zmiana statusu', 'sprzęt')
TYPES = (
    (COMMENT, COMMENT_NICE),
    (STATUS_CHANGE, STATUS_CHANGE_NICE),
    (HARDWARE_ADD, HARDWARE_ADD_NICE)
)

