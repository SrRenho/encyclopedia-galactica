from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_together import Together

CHROMA_PATH = "chroma"

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
TOGETHER_MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_response(query_text):
    print("received query")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME))
    print("db object created")

    results = db.similarity_search(query_text, k=2)
    print("db searched")
    if not results:
        print("no results")
        return "No relevant documents found."

    print("creating context text from found results")
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    print("creating prompt")
    prompt = (
        "Use the following sources to answer the question:\n\n"
        f"{context_text}\n\n"
        "Question: {query_text}."
    )

    print("creating llm object")
    llm = Together(model=TOGETHER_MODEL_NAME, temperature=0.7, max_tokens=200)
    print("querying llm")
    response_text = llm.invoke(prompt)

    print("returning response")
    return f"{response_text}\n\nSources:\n{context_text}"





