# backend/config/mongoDB.py

import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

load_dotenv()

# env variables
MONGODB_URI = os.getenv("MONGODB_URI")
APP_ENV = os.getenv("APP_ENV", "development")

# validate env
if not MONGODB_URI:
    print("❌ MONGODB_URI is missing from .env")
    sys.exit(1)

# universal MongoDB client
callingMongoClient = MongoClient(
    MONGODB_URI,
    server_api=ServerApi("1"),
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=20000,
    maxPoolSize=50,
    minPoolSize=1,
    retryWrites=True,
)


def connectToMongoDB():
    try:
        print("⏳ Connecting to MongoDB Atlas...")

        pingResult = callingMongoClient.admin.command("ping")

        print("✅************* Successfully connected to MongoDB! ***************✅")
        print("✅ Universal MongoDB client is online")
        print("✅ Models can now choose their own database and collection")

        if APP_ENV == "development":
            print(f"✅ MongoDB ping result: {pingResult}")

        return True

    except ServerSelectionTimeoutError as error:
        print(f"❌ Server selection timeout: {error}")
        print("Please check your MongoDB URI.")
        print("Check your network connection.")
        print("Check MongoDB Atlas IP address allowlist.")
        sys.exit(1)

    except PyMongoError as error:
        print(f"❌ An error occurred while connecting to MongoDB: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"❌ An unexpected error occurred: {error}")
        sys.exit(1)


def useDatabase(databaseName):
    return callingMongoClient[databaseName]


def disconnectFromMongoDB():
    try:
        print("⏳ Disconnecting from MongoDB...")

        callingMongoClient.close()

        print("✅ Disconnected from MongoDB successfully.")

    except PyMongoError as error:
        print(f"❌ An error occurred while disconnecting from MongoDB: {error}")

    except Exception as error:
        print(f"❌ An unexpected error occurred while disconnecting: {error}")

