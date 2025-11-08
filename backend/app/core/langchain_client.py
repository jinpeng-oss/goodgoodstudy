import os
import asyncio
import logging
from typing import Optional
from app.core.config import settings

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter

logger = logging.getLogger(__name__)

class LangChainClient:
    """A simple LangChain client that supports retrieval-augmented generation (RAG)
    using a local Chroma vectorstore and OpenAI embeddings + ChatOpenAI.

    Notes:
    - This class keeps blocking LangChain calls in a thread via asyncio.to_thread so
      it can be awaited from async FastAPI routes.
    - Configure vector DB directory via settings.VECTOR_DB_DIR (optional) or default './vector_db'.
    """

    def __init__(self, persist_directory: Optional[str] = None, embed_model: Optional[str] = None, llm_model: Optional[str] = None):
        self.api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY is not configured")

        self.persist_directory = persist_directory or getattr(settings, "VECTOR_DB_DIR", "./backend/app/core/vector_db")
        os.makedirs(self.persist_directory, exist_ok=True)

        # Model names (can be configured in settings)
        self.embed_model = embed_model or getattr(settings, "EMBEDDING_MODEL", "text-embedding-3-small")
        self.llm_model = llm_model or getattr(settings, "MODEL_NAME", "gpt-4o")

        # Embedding and vectorstore will be lazily initialized
        self._embeddings = None
        self._vectordb = None

    def _get_embeddings(self) -> OpenAIEmbeddings:
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        return self._embeddings

    def _get_vectordb(self) -> Chroma:
        if self._vectordb is None:
            # If the DB doesn't exist yet, Chroma will create it when ingesting
            self._vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=self._get_embeddings())
        return self._vectordb

    async def answer(self, question: str, context: Optional[str] = None, k: int = 4, return_sources: bool = False) -> str:
        """Answer a question using RetrievalQA. This is async-friendly.

        Parameters:
        - question: user question
        - context: optional additional context to include in prompt
        - k: number of retrieved chunks
        - return_sources: if True, attempt to return sources (may be implementation dependent)
        """
        if not question or not question.strip():
            raise ValueError("question is required")

        # Prepare the final prompt (we keep it simple and let the chain handle concatenation)
        q = question
        if context:
            q = f"{question}\n\n附加上下文：{context}"

        # Build retriever and chain in a blocking call (LangChain objects are typically sync)
        def run_sync():
            embeddings = self._get_embeddings()
            vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=embeddings)
            retriever = vectordb.as_retriever(search_kwargs={"k": k})

            # Use a ChatOpenAI wrapper; chain_type 'stuff' is simplest. Tune as needed.
            llm = ChatOpenAI(temperature=0.2, model=self.llm_model, openai_api_key=self.api_key)
            qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

            # Run the chain
            resp = qa_chain.run(q)
            return resp

        # Execute in threadpool to avoid blocking the event loop
        result = await asyncio.to_thread(run_sync)

        return result

    def ingest(self, source_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> dict:
        """Synchronous ingestion helper. Reads .txt/.md files under source_dir, splits into chunks,
        creates embeddings and stores them in Chroma persist_directory.

        Returns a summary dict with counts.
        """
        texts = []
        metadata = []
        for root, _, files in os.walk(source_dir):
            for fn in files:
                if fn.lower().endswith((".txt", ".md")):
                    path = os.path.join(root, fn)
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Basic metadata: source filepath
                    texts.append(content)
                    metadata.append({"source": path})

        if not texts:
            return {"ingested_files": 0, "ingested_chunks": 0}

        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = []
        metadatas = []
        for txt, md in zip(texts, metadata):
            c = splitter.split_text(txt)
            chunks.extend(c)
            metadatas.extend([md] * len(c))

        # Create Document objects expected by Chroma.from_documents
        try:
            from langchain.schema import Document
            docs = [Document(page_content=chunk, metadata=md) for chunk, md in zip(chunks, metadatas)]
        except Exception:
            # Fallback: use plain strings (Chroma.from_documents expects Document; if unavailable, try another path)
            docs = chunks

        embeddings = self._get_embeddings()
        vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=self.persist_directory)
        vectordb.persist()

        return {"ingested_files": len(texts), "ingested_chunks": len(chunks), "persist_directory": self.persist_directory}