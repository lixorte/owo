from pymongo import MongoClient
from loguru import logger
from flask import Blueprint


client = MongoClient('mongodb://mongo:27017/', connect=False)
