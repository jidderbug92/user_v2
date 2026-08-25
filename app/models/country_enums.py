from enum import Enum


class Country(str, Enum):
    """
    simple class to encapsulate all countires offically supported.
    """

    UNITED_STATES = "USA"
    CANADA = "CAN"
