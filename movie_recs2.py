import pymongo  # Import pymongo to interact with MongoDB
import openai   # Import OpenAI for embedding generation

# Set your OpenAI API key
openai.api_key = ''  # TODO: Insert your OpenAI API key here

client = pymongo.MongoClient("")  # Connect to MongoDB (provide connection string)
db = client.sample_mflix  # Access the 'sample_mflix' database
collection = db.embedded_movies  # Access the 'embedded_movies' collection

def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding for the input text using OpenAI's API
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # Specify the embedding model
        input=text
    )
    return response['data'][0]['embedding']  # Return the embedding vector

query = "imaginary characters from outer space at war"  # Example query string

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),  # Use embedding as query vector
    "path": "plot_embedding",  # Field containing embeddings in MongoDB
    "numCandidates": 100,  # Number of candidates to consider
    "limit": 4,  # Limit results to top 4
    "index": "PlotSemanticSearch",  # Name of the vector index
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')