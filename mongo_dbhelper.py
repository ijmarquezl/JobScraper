# DBHelper for MongoDB
"""This module is created to support communication with MongoDB."""

from pymongo import MongoClient as MC
import logging
import config


# Creamos una clase para agrupar funciones
class DBHelper:
    """Implementation of MongoDB functionality."""

    __db = ""

    logging.basicConfig(format=config.FORMAT)
    lg = logging.getLogger('tcpserver')

    def __init__(self, database="coaching"):
        """Connect to the DB."""
        client = MC(config.dbHost, config.dbPort)
        self.__db = client[database]

    def dbFindOne(self, col, params=None):
        """Find the first document in the collection col."""
        return self.__db[col].find_one(params)

    def dbFind(self, col, params=None):
        """Find all the documents in the collection col."""
        return self.__db[col].find(params)

    def dbInsert(self, col, params):
        """Insert a new document in the collection col."""
        return self.__db[col].insert_one(params)

    def dbUpdate(self, col, crit, params, upsert=True):
        """Update a document in the collection col."""
        # self.lg.debug("Criterio = {}\nParametros = {}\n", format(crit, \
        # str(params)))
        return self.__db[col].update_one(crit, params, upsert)

    def dbDelete(self, col, params):
        """Delete a single document in the collection col."""
        return self.__db[col].delete_one(params)
