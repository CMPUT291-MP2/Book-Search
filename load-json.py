import sys, os
import pymongo
from pymongo import MongoClient

class CreateStore:
    """This is the main class for part 1. Contains all the methods to make this part function
    aside from setting up the server (which should already be done beforehand)
    """

    def __init__(self, json:str, port:int, host:str=None) -> None:
        """Creates the CreateStore object

        Args:
            json (str): the location of the json file (relative to this file)
            port (int): the port number
            host (str, optional): overrides the host location and port. Defaults to None.
        """
        self.host = host
        self.json = json
        self.port = port
        self.client = MongoClient(host, port=self.port)
    
    def create_database(self) -> None:
        """Creates the database with the name "291db"
        """
        self.db = self.client["291db"]
    
    def create_collection(self) -> None:
        """Creates the collection "dblp" in the database "291db". Drops it if it already exists.
        
        Note: This method must be called AFTER the create_database() method
        """

        # if the collection already exists, drop it
        collist = self.db.list_collection_names()
        if "dblp" in collist:
            self.db.drop_collection("dblp")

        # create the collection
        self.collection = self.db["dblp"]
        
        # import the data using mongoimport
        os.system("mongoimport --port " + str(self.port) + " --db 291db --collection dblp --type=json --file " + self.json)
        
        # add another field which is the year converted from type int -> string
        # this allows for much easier searching in the future
        print("ADDING ANOTHER YEAR FIELD AS STRING")
        update = [{"$addFields" : {"convYear" : {"$toString" : "$year"}}}]
        self.collection.update_many({}, update)

        # add the index for faster searching in the future
        print("INDEXING DATABASE")
        self.collection.create_index([("authors", pymongo.TEXT), ("title", pymongo.TEXT), ("abstract", pymongo.TEXT), ("venue", pymongo.TEXT), ("convYear", pymongo.TEXT)], name="main_search_index", default_language="english")

    def shutdown(self) -> None:
        """Closes the client
        """
        self.client.close()

if __name__ == "__main__":
    create_store = CreateStore(sys.argv[1], int(sys.argv[2]))
    create_store.create_database()
    create_store.create_collection()
    create_store.shutdown()
