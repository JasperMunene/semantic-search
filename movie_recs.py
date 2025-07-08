import pymongo  # Import the pymongo library to interact with MongoDB
from sentence_transformers import SentenceTransformer  # Import the sentence transformer for embeddings



client = pymongo.MongoClient("")  # Connect to MongoDB (connection string should be provided)
db = client.sample_mflix  # Access the 'sample_mflix' database
collection = db.movies  # Access the 'movies' collection

# Load the pre-trained sentence transformer model for generating embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding for the input text
    """
    # Generate embedding and convert to Python list
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()

# Example code to add embeddings to documents (commented out)
# for doc in collection.find({'plot':{"$exists": True}}).limit(50):
#   doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
#   collection.replace_one({'_id': doc['_id']}, doc)
  
query = "imaginary characters from outer space at war"  # Example query string

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')