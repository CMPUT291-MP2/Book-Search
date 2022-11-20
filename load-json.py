import sys
import json
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
        
        # load in the data
        with open(self.json, "r") as file:
            for line in file:
                data = json.loads(line)
                self.collection.insert_one(data)
    
    def shutdown(self) -> None:
        """Closes the client
        """
        self.client.close()
    
    def test(self) -> None:
        """A simple testing function to execute commands when developing this program
        Feel free to change this method whenever you need
        """
        print(self.client.list_database_names())
        print(self.db.list_collection_names())

        # list the contents of the collection (could be very long!)
        self.collection = self.db.get_collection("dblp")
        cursor = self.collection.find({})
        for doc in cursor:
            print(doc)


if __name__ == "__main__":
    create_store = CreateStore(sys.argv[1], int(sys.argv[2]))
    create_store.create_database()
    create_store.create_collection()
    # create_store.test() # list all databases, collections, and their contents
    create_store.shutdown()
