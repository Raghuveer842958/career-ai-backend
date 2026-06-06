from ai.rag.vectorstore import retriever

def retrieve_resume_context(query):

    retrieved_docs = retriever.invoke(query)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(retrieved_docs, start=1):

        print(f"\nChunk {i}:\n")
        print(doc.page_content)
        print("-" * 50)

    return retrieved_docs