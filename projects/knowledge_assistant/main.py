from storage.database import Database
from storage.initializer import DatabaseInitializer
from storage.document_repository import DocumentRepository
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from services.generation_service import GenerationService
from models.document import Document
import os

def load_documents(directory, embedder, repo):
    """Load and chunk text files from a directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                text = f.read()
            # Simple chunking: split by paragraphs or fixed size
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            for idx, chunk in enumerate(chunks):
                embedding = embedder.embed_single(chunk)
                doc = Document(
                    title=filename,
                    content=chunk,
                    chunk_index=idx,
                    embedding=embedding
                )
                repo.insert(doc)
    print(f"Loaded documents from {directory}.")

def main():
    db = Database("knowledge.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    doc_repo = DocumentRepository(db)
    embedder = EmbeddingService()
    retriever = RetrievalService(doc_repo)
    generator = GenerationService()

    # Load documents if any
    data_dir = input("Enter documents directory path (or 'skip' if already loaded): ").strip()
    if data_dir.lower() != 'skip':
        load_documents(data_dir, embedder, doc_repo)

    print("\nAI Knowledge Assistant ready. Ask questions!")
    while True:
        question = input("\nQuestion (or 'quit'): ").strip()
        if question.lower() == 'quit':
            break
        if not question:
            continue
        query_emb = embedder.embed_single(question)
        chunks = retriever.retrieve(query_emb, top_k=3)
        if not chunks:
            print("No relevant documents found.")
            continue
        answer = generator.generate(question, chunks)
        print(f"\nAnswer:\n{answer}")
        print("\nSources:")
        for i, chunk in enumerate(chunks):
            print(f"{i+1}. {chunk.title} (chunk {chunk.chunk_index})")

    db.close()

if __name__ == "__main__":
    main()