import os
import logging
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env relative to current file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

MONGO_URI = os.getenv("MONGO_URI")

client = None
db = None


class InMemoryCollection:
    """A thread-safe, in-memory collection that mimics basic PyMongo operations."""

    def __init__(self, name):
        self.name = name
        self.documents = []

    def insert_one(self, document):
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = ObjectId()
        self.documents.append(doc)

        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id

        return InsertResult(doc["_id"])

    def _matches(self, doc, filter_query):
        if not filter_query:
            return True
        for key, val in filter_query.items():
            if key == "_id":
                if str(doc.get("_id")) != str(val):
                    return False
            elif isinstance(val, dict):
                # Simple operator support
                if "$regex" in val:
                    import re
                    pattern = re.compile(val["$regex"], re.IGNORECASE if val.get("$options") == "i" else 0)
                    if not pattern.search(str(doc.get(key, ""))):
                        return False
                if "$exists" in val:
                    exists = key in doc and doc[key] is not None
                    if val["$exists"] != exists:
                        return False
                if "$nin" in val:
                    if doc.get(key) in val["$nin"]:
                        return False
                if "$not" in val:
                    sub = val["$not"]
                    if "$regex" in sub:
                        import re
                        pattern = re.compile(sub["$regex"], re.IGNORECASE if sub.get("$options") == "i" else 0)
                        if pattern.search(str(doc.get(key, ""))):
                            return False
            else:
                if doc.get(key) != val:
                    return False
        return True

    def find_one(self, filter_query=None):
        for doc in reversed(self.documents):
            if self._matches(doc, filter_query):
                return doc
        return None

    def find(self, filter_query=None):
        matches = [doc for doc in self.documents if self._matches(doc, filter_query)]

        class Cursor:
            def __init__(self, items):
                self.items = list(items)

            def sort(self, field, direction=1):
                reverse = (direction == -1)
                self.items.sort(
                    key=lambda x: (
                        x.get(field).isoformat()
                        if isinstance(x.get(field), datetime)
                        else str(x.get(field, ""))
                    ),
                    reverse=reverse,
                )
                return self

            def limit(self, n):
                self.items = self.items[:n]
                return self

            def __iter__(self):
                return iter(self.items)

            def __len__(self):
                return len(self.items)

        return Cursor(matches)

    def count_documents(self, filter_query=None):
        return len([doc for doc in self.documents if self._matches(doc, filter_query)])

    def update_one(self, filter_query, update_doc):
        doc = self.find_one(filter_query)
        if doc and "$set" in update_doc:
            doc.update(update_doc["$set"])
            return True
        return False


class InMemoryDatabase:
    """Fallback in-memory DB when MongoDB connection is unreachable."""

    def __init__(self):
        self._collections = {}

    def __getitem__(self, name):
        if name not in self._collections:
            self._collections[name] = InMemoryCollection(name)
        return self._collections[name]

    def list_collection_names(self):
        return list(self._collections.keys())


# Connect to MongoDB with fast timeout, fallback to in-memory store
try:
    if MONGO_URI:
        # Prevent dnspython from hanging for 30s when offline or in sandbox
        try:
            import dns.resolver
            resolver = dns.resolver.get_default_resolver()
            resolver.lifetime = 1.5
            resolver.timeout = 1.5
        except Exception:
            pass

        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=1500,
            connectTimeoutMS=1500,
            socketTimeoutMS=1500,
        )
        # Verify connection
        client.admin.command("ping")
        db_name = os.getenv("DATABASE_NAME", "deepleaf")
        db = client[db_name]
        print(f"MongoDB Connected Successfully to '{db_name}'")
    else:
        raise ValueError("MONGO_URI not configured in .env")
except Exception as exc:
    logger.warning("MongoDB Atlas is not reachable (%s). Using in-memory database fallback.", exc)
    print(f"MongoDB offline/unreachable: using local in-memory database.")
    db = InMemoryDatabase()
