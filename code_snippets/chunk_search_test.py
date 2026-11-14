import os
import numpy
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

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

def get_embedding(text):
    response = client.embeddings.create(
        model = os.getenv("EMBED_MODEL"),
        input = text
    )

    return response.data[0].embedding

def add_embeddings(chunks):
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        chunk["vector"] = vector
    return chunks

def cosine_similarity(A, B):
    dot_prod = numpy.dot(A, B)
    norm_a = numpy.linalg.norm(A)
    norm_b = numpy.linalg.norm(B)
    return dot_prod / (norm_a * norm_b)

def get_chunks(doc):
    chunks = []
    chunk_id = 0;

    for part in doc["text"].split("\n\n"):
        part = part.strip()
        if(part):
            chunks.append({
                "source" : doc["source"],
                "chunk_id" : chunk_id,
                "text" : part
            })
            chunk_id += 1

    return chunks

def search(query,chunks,top_k=3):
    vector = get_embedding(query)
    result = []
    for chunk in chunks:
        score = cosine_similarity(vector,chunk["vector"])

        result.append({
            "score" : score,
            "source" : chunk["source"],
            "chunk_id" : chunk["chunk_id"],
            "text": chunk["text"],
        })

    result.sort(key=lambda rec:rec["score"],reverse=True)
    return result[:top_k]

def create_chunks(documents):
    chunks  = []
    for doc in documents:
        chunks.extend(get_chunks(doc))
    return chunks


def test(query,chunks,top_k=3):
    print(f"User Query : {query}")

    result = search(query,chunks,top_k)

    for r in result:
       print(f" {r['score']:.2f} - {r['source']} - {r['text']}")

documents = load_documents(KB_FOLDER)
chunks = create_chunks(documents)
chunks = add_embeddings(chunks)

user_query = "What are the benefits of Maternity Leave ?"
test(user_query, chunks, 3)