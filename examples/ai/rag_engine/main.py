from core.models import Document
from services.chunker import TextChunker
from services.embedder import MockEmbeddingGenerator
from services.vector_store import VectorStore


def main() -> None:
    print("=== INITIALIZING RETRIEVAL-AUGMENTED GENERATION (RAG) PIPELINE ===\n")

    # 1. Define Source Enterprise Knowledge Document
    sample_text = (
        "Enterprise System Security Policy 2026. "
        "Section 4.1: Production database access requires multi-factor authentication (MFA) "
        "and active SSH bastion tunneling. All static database API keys must be rotated "
        "every 30 days automatically. Section 4.2: Incident response protocol requires "
        "notifying the Security Operations Center (SOC) within 15 minutes of detecting "
        "any unauthorized data access attempt."
    )

    doc = Document(doc_id="SOP-2026-001", content=sample_text)

    # 2. Chunk Source Document
    chunker = TextChunker(chunk_size=120, overlap=30)
    chunks = chunker.split_document(doc)
    print(f"[INDEXING] Created {len(chunks)} text chunks from document '{doc.doc_id}'.")

    # 3. Generate Embeddings for Chunks
    embedder = MockEmbeddingGenerator(dimension=16)
    for chunk in chunks:
        chunk.embedding = embedder.embed_text(chunk.text)

    # 4. Populate Vector Database
    vector_db = VectorStore()
    vector_db.add_chunks(chunks)
    print("[INDEXING] Vectors indexed in memory store successfully.")

    # 5. Process User Query at Runtime
    user_query = "How often must static database API keys be rotated according to policy?"
    print(f"\n[QUERY] Incoming User Query: '{user_query}'")

    # Embed User Query
    query_vector = embedder.embed_text(user_query)

    # Retrieve Top-K Contexts
    top_k_results = vector_db.search(query_vector, top_k=2)

    print("\n--- RETRIEVED CONTEXT CHUNKS ---")
    retrieved_texts = []
    for rank, res in enumerate(top_k_results, start=1):
        print(f"Rank {rank} [Score: {res.score:.4f}] (ID: {res.chunk.chunk_id}):")
        print(f"  \"{res.chunk.text}\"")
        retrieved_texts.append(res.chunk.text)

    # 6. Construct Augmented Prompt
    context_block = "\n".join([f"- {text}" for text in retrieved_texts])
    augmented_prompt = (
        "<system_directive>\n"
        "Answer the query using ONLY the provided context below.\n"
        "</system_directive>\n\n"
        f"<retrieved_context>\n{context_block}\n</retrieved_context>\n\n"
        f"<user_query>\n{user_query}\n</user_query>"
    )

    print("\n--- HYDRATED RAG PROMPT ---")
    print(augmented_prompt)


if __name__ == "__main__":
    main()