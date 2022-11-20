CMPUT 291 Mini-Project 2

Running Instructions:
    1. In one terminal, start mongodb locally with "mongod --dbpath data/db"
    2. In another terminal, run the first part with "python3 load-json.py <path_to_json_file> <port_number>"
    
    This will have created the database and inserted the values from the specified json file.
    To see if all values were inserted, comment out the create_collection() method and uncomment the test() method; this will display all value inserted into the collection (could be very long!)

Other Notes:
    - The "dblp-ref-1m.json" test file is not included due to size limitations
    - "reference-code.py" is simply the provided pymongo code from the lab
    - May have to change the way the collection is created as it is not using the "mongoimport" functionality
    - The second part is in progress