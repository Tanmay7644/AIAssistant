import os
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()


client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

def cosine_similarity(A,B):
    dot_product = np.dot(A,B)
    len_A = np.linalg.norm(A)
    len_B = np.linalg.norm(B)

    return dot_product/(len_A*len_B)

def get_embedding(text):
    response = client.embeddings.create(
        model = os.getenv("EMBED_MODEL"),
        input = text,
    )

    return response.data[0].embedding

A = "Python is a programming language"
B = "Python is used in AI related work"
C = "Apples are sweet"

embA = get_embedding(A)
embB = get_embedding(B)
embC = get_embedding(C)

csAB = cosine_similarity(embA,embB)
csAC = cosine_similarity(embA,embC)

print(f"{csAB:.2f}")
print(f"{csAC:.2f}")