from enum import Enum

class OrderStatus(str, Enum):
    TEMP = "TEMP"
    CLOSE = "CLOSE"


class ItemCategory(str, Enum):
    ELECTRONICS = "electronics"
    SPORTS = "sports"
    HOME = "home"
    TOYS = "toys"
    FASHION = "fashion"
    FOOD = "food"
    BEAUTY = "beauty"
    OTHER = "other"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
