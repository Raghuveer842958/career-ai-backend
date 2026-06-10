# from motor.motor_asyncio import AsyncIOMotorClient
# from dotenv import load_dotenv
# import os

# load_dotenv()

# try:

#     MONGO_URI = os.getenv("MONGO_URI")
#     # print("MONGO_URI is :", MONGO_URI)
#     client = AsyncIOMotorClient(
#         MONGO_URI
#     )

#     print("database list :",client.list_database_names())
#     # print(db.list_collection_names())

#     # "mongodb://localhost:27017"

#     db = client["fastapi_db"]
#     users_collection = db["users"]
#     jobs_collection = db["jobs"]
#     interviews_collection = db["interviews"]
    
#     job_indexes = jobs_collection.index_information()

#     print("job indexes are :", job_indexes)
#     # jobs_collection.create_index("job_id", unique=True)

#     # if "job_id_1" not in job_indexes:
#     #     print("job_id index is not in indexes")
#     #     jobs_collection.create_index("job_id", unique=True)

#     print("MongoDB Connected Successfully")

# except Exception as e:
#     print("Database Connection Error :", e)







from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

jobs_collection = None
users_collection = None
interviews_collection = None


def connect_db():
    global client, db
    global jobs_collection, users_collection, interviews_collection

    MONGO_URI = os.getenv("MONGO_URI")

    client = AsyncIOMotorClient("mongodb://localhost:27017/mydatabase")
    db = client["career_ai_db"]

    jobs_collection = db["jobs"]
    users_collection = db["users"]
    interviews_collection = db["interviews"]

    print("jobs_collection:", jobs_collection)
    print("interviews_collection:", interviews_collection)

    print("MongoDB Connected Successfully")