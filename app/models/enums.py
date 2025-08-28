from enum import Enum


class MatchType(str, Enum):
    FRIENDLY = "친선 경기"
    RANDOM_MATCH_REQUEST = "랜덤 매칭 요청"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class CalendarEventType(str, Enum):
    ACADEMIC = "ACADEMIC"
    MATCH = "MATCH"
    AVAILABILITY = "AVAILABILITY"
