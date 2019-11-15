from pymongo import MongoClient
from loguru import logger
from flask import Blueprint
from owo.api.utils import schema_validator
from owo.api.schemas import *


logger.add("api_admin.log", colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day", backtrace=True, diagnose=True)

client = MongoClient('mongodb://mongo:27017/')

