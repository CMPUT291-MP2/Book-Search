# Library Search

## Prerequisites:
    - Python 3.8+
    - pymongo
    - MongoDB (https://www.mongodb.com/docs/manual/installation/)
    - MongoDB Command Line Database Tools (https://www.mongodb.com/try/download/database-tools)

## Running Instructions (Part 1):
    1. In one terminal, start mongodb locally with "mongod --dbpath data/db"
    2. In another terminal, run the first part with "python3 load-json.py <path_to_json_file> <port_number>"
    
    This will have created the database and inserted the values from the specified json file.
    To see if all values were inserted, comment out the create_collection() method and uncomment the test() method; this will display all value inserted into the collection (could be very long!)

## Running Instructions (Part 2):
    1. Run Part 1
    2. Start the program with "python3 document-database.py <port_number>"

    Note that <port_number> needs to be the same between part 1 and part 2.

## Other Notes:
    - The "dblp-ref-1m.json" test file is not included due to size limitations
    - "reference-code.py" is simply the provided pymongo code from the lab
    - The second part is in progress
