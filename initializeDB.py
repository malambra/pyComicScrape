import pymongo
import argparse

def create_database(client, database_name, collection_name):
    try:
        # Get the database (it will create the database if it does not exist)
        db = client[database_name]
        
        # Check if the collection exists in the database
        collections = db.list_collection_names()
        if collection_name not in collections:
            # The collection does not exist, so we create it
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created in the database '{database_name}'")
        else:
            print(f"The collection '{collection_name}' already exists in the database '{database_name}'")
    except Exception as e:
        print(f"Error creating the database and collection: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description='Create a database and a collection in MongoDB.')
    parser.add_argument('database_name', help='The name of the database.')
    parser.add_argument('collection_name', help='The name of the collection.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        client = pymongo.MongoClient("mongodb://root:example@localhost:27018/")
        create_database(client, args.database_name, args.collection_name)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")