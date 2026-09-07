from models.document import Document
import json
import numpy as np

class DocumentRepository:
    def __init__(self, db):
        self.db = db

    def insert(self, doc):
        self.db.execute(
            "INSERT INTO documents (title, content, chunk_index, embedding) VALUES (?, ?, ?, ?)",
            (doc.title, doc.content, doc.chunk_index, json.dumps(doc.embedding.tolist()))
        )
        self.db.commit()
        doc.id = self.db.last_row_id()
        return doc

    def get_all(self):
        self.db.execute("SELECT * FROM documents")
        rows = self.db.fetchall()
        docs = []
        for row in rows:
            doc = Document(
                doc_id=row["id"],
                title=row["title"],
                content=row["content"],
                chunk_index=row["chunk_index"],
                embedding=np.array(json.loads(row["embedding"]))
            )
            docs.append(doc)
        return docs

    def delete_all(self):
        self.db.execute("DELETE FROM documents")
        self.db.commit()