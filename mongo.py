import pymongo
from pymongo import MongoClient

class MusicDatabase:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.musicians = self.db['Musicians']

    def create_musician(self, musician_data):
        result = self.musicians.insert_one(musician_data)
        return result.inserted_id

    def get_musician(self):
        print("Retrieved Musician:")
        for d in self.musicians.find():
            print(d)

    def update_musician(self, musician_id, updated_data):
        result = self.musicians.update_one({"SSN": musician_id}, {"$set": updated_data})
        return result.modified_count

    def delete_musician(self, musician_id):
        result = self.musicians.delete_one({"SSN": musician_id})
        return result.deleted_count

    def close_connection(self):
        self.client.close()


uri = "mongodb://localhost:27017/"
db_name = "MusicDatabase"

music_db = MusicDatabase(uri, db_name)

while True:
    print("\nOptions:")
    print("1. Create Musician")
    print("2. Retrieve Musician")
    print("3. Update Musician")
    print("4. Delete Musician")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        musician_data = {
            "SSN": input("Enter SSN: "),
            "name": input("Enter name: "),
            "address": input("Enter address: "),
            "phone": input("Enter phone: "),
        }
        music_db.create_musician(musician_data)
        print("Musician created successfully.")

    elif choice == "2":
        musician = music_db.get_musician()

    elif choice == "3":
        musician_id = input("Enter Musician SSN to update: ")
        updated_data = {
            "address": input("Enter updated address: "),
            "phone": input("Enter updated phone: "),
        }
        modified_count = music_db.update_musician(musician_id, updated_data)
        if modified_count > 0:
            print("Musician updated successfully.")
        else:
            print("Musician not found.")

    elif choice == "4":
        musician_id = input("Enter Musician SSN to delete: ")
        deleted_count = music_db.delete_musician(musician_id)
        if deleted_count > 0:
            print("Musician deleted successfully.")
        else:
            print("Musician not found.")

    elif choice == "5":
        music_db.close_connection()
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please select a valid option.")
