# from ai.vectorstore import get_retriever

from ai.rag.vectorstore import get_retriever


def retrieve_resume_context(query):

    retriever = get_retriever()
    retrieved_docs = retriever.invoke(query)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(retrieved_docs, start=1):

        print(f"\nChunk {i}:\n")
        print(doc.page_content)
        print("-" * 50)

    return retrieved_docs