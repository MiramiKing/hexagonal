import os
from enum import Enum

class StoreType(Enum):
    REDIS = 'redis'
    SQL = 'sql'

class ApiType(Enum):
    FAST = 'fast'
    FLASK = 'flask'


store_type = StoreType(os.getenv('STORE_TYPE', 'redis'))

api_type = ApiType(os.getenv('API_TYPE', 'fast'))