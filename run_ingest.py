import os
from pinecone import Pinecone
from pinecone_client import init_pinecone, upsert_chunks, INDEX_NAME
from ingest import chunk_log_lines

LOG_FILE_PATH = "logs/sample_logs.txt"


def load_log_file(path):    #error handling for loading and file and if not found
    if not os.path.exists(path):
        raise FileNotFoundError(f"Log file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def main():
    lines = load_log_file(LOG_FILE_PATH)
    chunks = chunk_log_lines(lines, source=LOG_FILE_PATH) 
    print(f"Created {len(chunks)} chunks")

    index = init_pinecone()
    print("Done indexing, now uploading to Pinecone...")

    total = upsert_chunks(index, chunks, batch_size=100)
    print(f"Uploaded {total} vectors to Pinecone index '{INDEX_NAME}'")


if __name__ == "__main__":
    main()