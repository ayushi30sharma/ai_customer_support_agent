"""
Policy Retriever: Loads policies.csv into ChromaDB and searches it.
Why: We don't want the LLM to guess policies. We want to retrieve the exact
text from the CSV based on the customer's question.
"""
import os
import pandas as pd
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "policies.csv"
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma_db")
if not Path(CHROMA_PATH).is_absolute():
    CHROMA_PATH = PROJECT_ROOT / CHROMA_PATH

# We use Gemini's free text embedding model
# Note: Requires GOOGLE_API_KEY in .env
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def initialize_policy_db():
    """
    Reads policies.csv, embeds the text, and stores it in ChromaDB.
    Run this once (or whenever policies.csv changes).
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing policies.csv at {CSV_PATH}")
    
    print(f"📖 Loading policies from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)
    
    # Combine columns into one searchable text block per policy
    # This gives the embedding model the full context of the policy
    documents = []
    metadatas = []
    ids = []
    
    for _, row in df.iterrows():
        # Combine rule, conditions, and action so the search is accurate
        full_text = f"Policy: {row['policy_name']} ({row['topic']}). Rule: {row['rule']} Conditions: {row['conditions']} Action: {row['action']}"
        
        documents.append(full_text)
        metadatas.append({
            "policy_id": row["policy_id"],
            "policy_name": row["policy_name"],
            "topic": row["topic"],
            "requires_human": str(row["requires_human"])
        })
        ids.append(row["policy_id"])

    # Initialize Chroma
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    # Delete existing collection if we are re-initializing
    try:
        client.delete_collection(name="store_policies")
    except Exception:
        pass
        
    collection = client.create_collection(name="store_policies")
    
    # Embed and add to Chroma
    print("🧠 Embedding policies via Gemini (this takes a few seconds)...")
    embeddings = embeddings_model.embed_documents(documents)
    
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("✅ Policy database initialized and saved to disk.")

def search_policy(query: str, top_k: int = 3) -> list[dict]:
    """
    Search ChromaDB for the most relevant policies.
    Returns a list of matching policies with their text and metadata.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    
    try:
        collection = client.get_collection(name="store_policies")
    except Exception:
        raise RuntimeError("Policy DB not initialized. Run initialize_policy_db() first.")

    # Embed the user's query
    query_embedding = embeddings_model.embed_query(query)
    
    # Search Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    # Format results for the LLM
    formatted_results = []
    for i in range(len(results["documents"][0])):
        formatted_results.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i] # Lower is better
        })
        
    return formatted_results

if __name__ == "__main__":
    # If run directly, initialize the DB
    initialize_policy_db()