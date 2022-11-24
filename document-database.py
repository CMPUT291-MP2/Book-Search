import sys
from pymongo import MongoClient, ASCENDING, DESCENDING
from pprint import pprint

class DocumentDatabase:
    """The main program for this project. Handles all aspects of part 2 including searching for articles
    and authors, listing venues, as well as adding an article.
    """

    def __init__(self, port:int, host:str=None) -> None:
        """Creates the DocumentDatabase object

        Args:
            port (int): the port number given on instantiation
            host (str, optional): overrides the host location and port. Defaults to None.
        """
        self.port = port
        self.host = host

        # creating the client and the connection
        self.client = MongoClient(host=host, port=port)
        self.db = self.client["291db"]
        self.collection = self.db["dblp"]
    
    def program_loop(self) -> None:
        """The main program loop. Presents all phase 2 options for the user to select. They can
        also exit the program here if they wish.
        """
        while True:
            print("\n------------------------------")
            print("Please select an option:")
            print("1. Search for articles")
            print("2. Search for authors")
            print("3. List the venues")
            print("4. Add an article")
            print("5. Exit program")
            print("------------------------------")

            # take in the user's selection
            selection = input(">: ")

            # find which action they selected
            if selection == "1":
                self._articles_loop()
            elif selection == "2":
                self._author_loop()
            elif selection == "3":
                continue
            elif selection == "4":
                self._add_articles()
            elif selection == "5":
                self._shutdown()
                break
            else:
                print("\nInvalid input, please try again...\n")
                continue
    
    def _add_articles(self):
        while True:
            print("\n------------------------------")
            print("Please select an option:")
            print("1. Add an article")
            print("2. Go back to main menu")
            print("------------------------------")
            selection = input(">: ")
            if selection == '2':
                return
            if selection == '1':
                break
            else:
                print("\nInvalid input, please try again...\n")
                continue

        print()
        # add an article
        print("\n------------------------------")
        while True:
            print("Please enter a unique id:")
            aid = input(">: ")
            ret = self.collection.find_one({'id': aid})
            # make sure it is unique
            if ret is not None:
                print("This id is taken, try another one.")
            else:
                break


        print("Please enter a title: ")
        title = input(">: ")

        print("Please enter a list of authors (comma separated): ")
        author_list = []
        authors = input(">: ")
        authors = authors.strip()
        authors = authors.split(',')
        for author in authors:
            trimmed = author.strip()
            author_list.append(trimmed)

        while True:
            print("Please enter a year: ")
            year = input(">: ")
            try:
                year = int(year)
            except:
                print("Invalid input...")
                continue
            if year > 0:
                break
            else:
                print("Invalid input...")
                continue

        data = dict(id=aid, title=title, authors=author_list, year=year, convYear=str(year), abstruct='', venue='', reference=[], n_citation=0)
        self.collection.insert_one(data)
        print("Success!")
        print("------------------------------")
    
    def _articles_loop(self) -> None:
        """The main loop for searching for articles. Adds all required functionality for this part.
        """
        while True:
            print("\n------------------------------------------------------------")
            print("Please enter article search keywords (comma separated):")
            print("------------------------------------------------------------")
            search = input(">: ")

            # clean up the input
            search = search.strip()

            # separate the keywords and reformat them cleanly into a single string.
            # this is used later on to query the database
            search_string = ""
            keywords = search.split(",")
            for i in range(len(keywords)):
                keywords[i] = keywords[i].strip()
                search_string += '"' + keywords[i] + '"' + " "
            search_string = search_string.strip()
            
            # format the final query, using the previously made query string
            final_query = {"$text" : {"$search" : search_string}}

            # get the results from the database
            cursor = self.collection.find(final_query)
            num_results = len(list(cursor.clone()))

            # present the results to the user
            results = []
            if num_results != 0:
                index = 0
                print("\n============================================================")
                for result in cursor:
                    results.append(result)
                    print()
                    print("ID:    " + result["id"])
                    print("TITLE: " + result["title"])
                    print("YEAR:  " + result["convYear"])
                    print("VENUE: " + result["venue"])
                    print("INDEX: " + str(index))
                    print()
                    index += 1
                print("============================================================")
            else: # if the query did not return anything
                while True:
                    print("\n------------------------------")
                    print("Please select an option:")
                    print("1. Try another query")
                    print("2. Go back to main menu")
                    print("------------------------------")
                    selection = input(">: ")

                    # find which action they selected
                    if selection == "1":
                        break
                    elif selection == "2":
                        return
                    else:
                        print("\nIncorrect input, please try again...\n")
                        continue
                continue

            # start the selection loop
            while True:
                print("\n------------------------------")
                print("Please select an option:")
                print("1. Select an article")
                print("2. Try another query")
                print("3. Go back to main menu")
                print("------------------------------")
                selection = input(">: ")

                # find which action they selected
                if selection == "1":
                    while True:
                        # prompt the user to select a result from the displayed list
                        print("\n------------------------------------------------------------")
                        print("Please enter the index of the above results:")
                        print("------------------------------------------------------------")
                        index = input(">: ")

                        # if the input is valid, it can be turned into an int, if it can't, then reprompt the user
                        try:
                            index = int(index)
                        except:
                            print("\nInvalid input, please try again...\n")
                            continue
                        
                        # if their index is within the number of articles, display the selected article's information
                        if (0 <= index <= (num_results - 1)):
                            selection = results[index]
                            referenced_articles = self._get_referenced_articles(selection)
                            print("\n============================================================")
                            print("\nID:")
                            pprint(selection["id"])
                            
                            print("\nTITLE:")
                            pprint(selection["title"])

                            print("\nAUTHORS:")
                            pprint(selection["authors"])

                            print("\nABSTRACT:")
                            pprint(selection["abstract"])

                            print("\nYEAR:")
                            pprint(selection["convYear"])

                            print("\nVENUE:")
                            pprint(selection["venue"])

                            print("\nREFS:")
                            pprint(referenced_articles)
                            print("\n============================================================")
                            break
                        else:
                            print("\nInvalid input, please try again...\n")
                            continue
                elif selection == "2":
                    break
                elif selection == "3":
                    return
                else:
                    print("\nInvalid input, please try again...\n")
                    continue
    
    def _get_referenced_articles(self, article:dict) -> list:
        """A simple helper method to get a list of all articles that reference
        the input article

        Args:
            article (dict): the input article

        Returns:
            list: a list of referencing articles
        """
        # find all articles that reference the input
        id = article["id"]
        cursor = self.collection.find({"references" : id}, {"id" : ASCENDING, "title" : ASCENDING, "convYear" : ASCENDING})

        # add them to an array
        articles = list(cursor)
        
        return articles

    def _get_author_articles(self, author:dict) -> list:
        """A simple helper method to get a list of all articles that have
        the given author

        Args:
            author (dict): the input author

        Returns:
            list: the list of articles
        """
        cursor = self.collection.aggregate([
            {"$match" : {"authors" : author["_id"]}},
            {"$project" : {"title" : "$title", "year" : "$year", "venue" : "$venue"}},
            {"$sort" : {"year" : DESCENDING}}
        ])

        # add them to an array
        return list(cursor)
       
        
    def _author_loop(self) -> None:
        """The main loop for search for authors. Adds all required functionality for this part.
        """
        while True:
            print("\n------------------------------------------------------------")
            print("Please enter a single search keyword:")
            print("------------------------------------------------------------")
            search = input(">: ").strip()

            cursor = self.collection.aggregate([
                {"$match" : {"$text" : {"$search" : search}}},
                {"$project" : {"authors" : "$authors"}},
                {"$match" : {"authors" : {"$regex" : search, "$options" : "i"}}},
                {"$unwind" : "$authors"},
                {"$match" : {"authors" : {"$regex" : search, "$options" : "i"}}},
                {"$project" : {"name" : "$authors"}},
                {"$group" : {"_id" : "$name", "count" : {"$sum" : ASCENDING}}},
                {"$sort" : {"count" : DESCENDING}}
            ])

            results = list(cursor)
            num_results = len(results)

            if results:
                index = 0
                print("\n============================================================")
                for result in results:
                    print()
                    print("NAME:      " + result["_id"])
                    print("NUM PUBS:  " + str(result["count"]))
                    print("INDEX:     " + str(index))
                    print()
                    index += 1
                print("============================================================")
            else:
                while True:
                    print("\n------------------------------")
                    print("Please select an option:")
                    print("1. Try another query")
                    print("2. Go back to main menu")
                    print("------------------------------")
                    selection = input(">: ")

                    # find which action they selected
                    if selection == "1":
                        break
                    elif selection == "2":
                        return
                    else:
                        print("\nIncorrect input, please try again...\n")
                        continue
                continue
            
            # start the selection loop
            while True:
                print("\n------------------------------")
                print("Please select an option:")
                print("1. Select an author")
                print("2. Try another query")
                print("3. Go back to main menu")
                print("------------------------------")
                selection = input(">: ")

                if selection == "1":
                    while True:
                        # prompt the user to select a result from the displayed list
                        print("\n------------------------------------------------------------")
                        print("Please enter the index of the above results:")
                        print("------------------------------------------------------------")
                        index = input(">: ")

                        # if the input is valid, it can be turned into an int, if it can't, then reprompt the user
                        try:
                            index = int(index)
                        except:
                            print("\nInvalid input, please try again...\n")
                            continue
                        
                        # if their index is within the displayed authors, display the selected author's information
                        if (0 <= index <= (num_results - 1)):
                            author = results[index]
                            author_results = self._get_author_articles(author)
                            print("\n============================================================")
                            for result in author_results:
                                print()
                                print("AUTHOR: " + author["_id"])
                                print("TITLE: " + result["title"])
                                print("YEAR: " + str(result["year"]))
                                print("VENUE: " + result["venue"])
                                print()
                            print("============================================================")
                            break
                        else:
                            print("\nIncorrect input, please try again...\n")

                elif selection == "2":
                    break
                elif selection == "3":
                    return
                else:
                    print("\nIncorrect input, please try again...\n")
                    continue

                    
    def _shutdown(self) -> None:
        """The exit function that closes the client. Should be called when exiting program
        """
        print("\nCleaning up and exiting...\n")
        self.client.close()


if __name__ == "__main__":
    db = DocumentDatabase(int(sys.argv[1]))
    db.program_loop()
