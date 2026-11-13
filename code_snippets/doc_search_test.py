from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)


# step 1: Loading all the documents
KB_FOLDER = os.getenv("KB_FOLDER")

def load_documents(folder = KB_FOLDER):
    documents = []

    for name in os.listdir(folder):
        if not name.endswith(".txt"):
            continue

        path = os.path.join(folder,name)

        with open(path,"r",encoding="utf-8") as f:
            documents.append({
                "source" : name,
                "text" : f.read()
            })

    return documents


# step 3: Add Embedding vector for each document

def get_embedding(text):
    response = client.embeddings.create(
        model = os.getenv("EMBED_MODEL"),
        input = text
    )

    return response.data[0].embedding


def add_embedding(documents):
    for doc in documents:
        text = doc["text"]
        embedding = get_embedding(text)

        doc["vector"] = embedding

    return documents

# step 4: Searching top_k relevant documents

def cosine_similarity(A,B):
    lenA = numpy.linalg.norm(A)
    lenB = numpy.linalg.norm(B)

    dot = numpy.dot(A,B)

    return dot/(lenA*lenB)

def search(query,documents,top_k = 3):
    query_vector = get_embedding(query)
    results = []
    for doc in documents:
        score = cosine_similarity(query_vector,doc["vector"])

        results.append({
            "score" : score,
            "source" : doc["source"]
        })

    results.sort(key=lambda rec:rec["score"], reverse=True)

    return results[:top_k]

def test(query,document,top_k=3):
    print(query)

    results = search(query,document,3)

    for r in results:
        print(f"{r['score']:.2f} {r['source']}")


documents = load_documents(KB_FOLDER)
documents = add_embedding(documents)

query = "What are the working hours of company?"

test(query,documents,3)