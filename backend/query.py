from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_together import Together
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
CHROMA_PATH = "chroma"

# Use a compact embedding model for free usage (you could use 'sentence-transformers/all-MiniLM-L6-v2')
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOGETHER_MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

PROMPT_TEMPLATE = (
    "Answer the question based only on the following sources:\n\n"
    "{context}\n\n"
    "---\n\n"
    "Based on the above sources, answer this question: {question}."
)

db = None
llm = None

def __init__():
    global db, llm
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    llm = Together(
        model=TOGETHER_MODEL_NAME,
        temperature=0.7,
        max_tokens=512
    )

def generate_response(query_text):
    results = search_context(query_text)
    context_text = create_context_text(results)
    prompt = create_prompt(query_text, context_text)

    print("will be prompted with: ", prompt)

    response_text = llm.invoke([HumanMessage(content=prompt)])
    # sources = [doc.metadata.get("source", None) for doc, _ in results]

    return format_response(response_text, context_text)

def format_response(response_text, context_text):
    return (f"{response_text}\n\n\n\nSources:"
     f"\n {context_text}")


def search_context(query_text):
    # Search similar documents
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if not results:# or results[0][1] < 0.7:
        print("Unable to find matching results.")
        return []

    return results


def create_context_text(results):
    return "\n\n---\n\n".join([doc.page_content for doc, _ in results])


def create_prompt(query_text, context_text):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=query_text)


