class Document:
    def __init__(self, doc_id=None, title="", content="", chunk_index=0, embedding=None):
        self.id = doc_id
        self.title = title
        self.content = content
        self.chunk_index = chunk_index
        self.embedding = embedding

    def __repr__(self):
        return f"Document(id={self.id}, title='{self.title}', chunk={self.chunk_index})"