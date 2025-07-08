from pymongo import MongoClient
from scripts.constants.app_configuration import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
