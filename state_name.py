from enum import Enum


class StateName(Enum):
    SEARCH = 1
    CHASE = 2
    TERMINATE = 3
    FILM = 4
