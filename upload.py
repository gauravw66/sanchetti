import openai
import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables (if using python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()

# Set your OpenAI API key securely
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize Qdrant client (update with your Qdrant instance URL and API key if needed)
client = QdrantClient(
    url= os.environ.get("QDRANT_CLIENT_URL"),
    # api_key='YOUR_QDRANT_API_KEY'  # Uncomment and set if your Qdrant instance requires an API key
)

# Load JSON data with utf-8 encoding
with open('FINAL.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inspect the first record to determine the correct key
print("First record structure:")
print(json.dumps(data[0], indent=2))

# Function to create embeddings using OpenAI's model
def create_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"  # Update to the correct model name
    )
    return response['data'][0]['embedding']

# Prepare data points for Qdrant
points = []
for i, record in enumerate(data):
    # Change 'text' to 'markdown' based on the JSON structure
    text = record.get('markdown')  # Use 'markdown' key to get the text data
    if text is None:
        print(f"Record {i} is missing the 'markdown' key. Skipping this record.")
        continue  # Skip if 'markdown' key is missing
    try:
        embedding = create_embedding(text)
    except Exception as e:
        print(f"Error creating embedding for record {i}: {e}")
        continue
    points.append(
        PointStruct(
            id=i,  # Unique ID for each record
            vector=np.array(embedding),  # Embedding vector
            payload=record  # Original record as payload
        )
    )

if not points:
    print("No valid points to upload. Exiting.")
    exit()

# Create a collection in Qdrant
collection_name = 'demo_new'
try:
    client.recreate_collection(
        collection_name=collection_name,
        vector_size=len(points[0].vector),  # Size of embedding vector
        distance='Cosine'  # Or use 'Euclidean' or 'Dot' based on your use case
    )
except Exception as e:
    print(f"Error creating collection '{collection_name}': {e}")
    exit()

# Upload points to Qdrant
try:
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("Data successfully uploaded to Qdrant!")
except Exception as e:
    print(f"Error uploading points to Qdrant: {e}")
