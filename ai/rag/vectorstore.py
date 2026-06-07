# from langchain_community.vectorstores import FAISS

# from ai.factories.embedding_factory import get_embeddings
# from ai.config.config import VECTOR_DB_PATH

# embeddings = get_embeddings()

# vectorstore = FAISS.load_local(
#     VECTOR_DB_PATH,
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# retriever = vectorstore.as_retriever(
#     search_kwargs={"k": 3}
# )



from langchain_community.vectorstores import FAISS

from ai.factories.embedding_factory import get_embeddings
from ai.config.config import VECTOR_DB_PATH

_retriever = None


def get_retriever():
    global _retriever

    if _retriever is None:
        embeddings = get_embeddings()

        vectorstore = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        _retriever = vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

    return _retriever