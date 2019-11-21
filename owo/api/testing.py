from pymongo import MongoClient
from loguru import logger
from flask import Blueprint


logger.add("api_testing.log", colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day",
           backtrace=True, diagnose=True)

client = MongoClient('mongodb://mongo:27017/', connect=False)
