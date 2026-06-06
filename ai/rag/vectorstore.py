from langchain_community.vectorstores import FAISS

from ai.factories.embedding_factory import get_embeddings
from ai.config.config import VECTOR_DB_PATH

embeddings = get_embeddings()

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)