# retriever_agent.py
from langchain_google_community import VertexAISearchRetriever
from functools import lru_cache

# Initialiser le VertexAI Retriever
DATA_STORE_ID = "grounding-unfpa_1733828609811"
DATA_STORE_LOCATION = "global"

retriever = VertexAISearchRetriever(
    project_id="unfpa-444213",
    location_id=DATA_STORE_LOCATION,
    data_store_id=DATA_STORE_ID,
    get_extractive_answers=True,
    max_documents=100,
    max_extractive_segment_count=1,
    max_extractive_answer_count=5,
)

@lru_cache(maxsize=10)
def retrieve_chunks(query):
    try:
        docs = retriever.get_relevant_documents(query)
        if not docs:
            return []  # Return an empty list if no documents are found
        docs = docs[:5]  # Limit to top 5 chunks
        return [{"chunk": doc.page_content, "source": doc.metadata['source']} for doc in docs]
    except Exception as e:
        print(f"An error occurred during retrieval: {e}")
        return []
