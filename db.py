from pymongo import MongoClient

def connect_db():
    uri = "mongodb+srv://Vercel-Admin-media-base:Qu5Y30VYqmF4GA1X@media-base.ufxe4cp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    try:
        client.admin.command("ping")
        print("Connected successfully")
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    db = client['media-base']
    return db

