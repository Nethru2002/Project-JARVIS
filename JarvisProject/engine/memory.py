import chromadb
import uuid

client = chromadb.PersistentClient(path="./jarvis_memory")
collection = client.get_or_create_collection(name="user_data")

def store_info(text):
    """Store information into Jarvis's long-term memory"""
    collection.add(
        documents=[text],
        ids=[str(uuid.uuid4())]
    )
    return "Sir, I've committed that to my memory."

def retrieve_memory(query):
    """Search memory for relevant context"""
    results = collection.query(query_texts=[query], n_results=1)
    if results['documents'][0]:
        return f"Relevant Memory: {results['documents'][0][0]}"
    return ""