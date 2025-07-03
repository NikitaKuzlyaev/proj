from enum import Enum


class OfferActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELED = "CANCELED"
    INACTIVE = "INACTIVE"

