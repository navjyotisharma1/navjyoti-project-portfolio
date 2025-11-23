import os
from dotenv import load_dotenv

# ✅ Updated imports for LangChain 1.0+
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Task, Crew, LLM

# ✅ Load environment variables
load_dotenv()

# API Keys (Use environment variables ideally)
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "8df33e2616adf56866a4f20588dc39b433214688")
GEMINI_API_KEY = os.getenv("GEMINI", "AIzaSyCeCJgYHu_rqdNWrJR98vp8fZ0pRuTTXQk")

# ✅ Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=500,
    timeout=None,
    max_retries=2,
)

crew_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GEMINI_API_KEY,
    max_tokens=500,
    temperature=0.7
)

# =========================
# Core Helper Functions
# =========================

def check_local_knowledge(query, context):
    """Determine whether the question can be answered from local knowledge"""
    prompt = f"""
Role: Question-Answering Assistant
Task: Determine if the question can be answered using the provided text.

Text:
{context}

Question:
{query}

Respond only with one word: "Yes" or "No".
"""
    response = llm.invoke(prompt)
    return response.content.strip().lower() == "yes"


# =========================
# Web Scraping & Agent Setup
# =========================

def setup_web_scraping_agent():
    """Setup agents for web search and scraping"""
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    web_search_agent = Agent(
        role="Expert Web Search Agent",
        goal="Find the best web sources for user queries",
        backstory="A professional at finding accurate online information.",
        allow_delegation=False,
        verbose=True,
        llm=crew_llm
    )

    web_scraper_agent = Agent(
        role="Expert Web Scraper",
        goal="Extract and summarize data from web pages",
        backstory="An AI that efficiently extracts and summarizes relevant content.",
        allow_delegation=False,
        verbose=True,
        llm=crew_llm
    )

    search_task = Task(
        description="Search the web for relevant sources about '{topic}'.",
        expected_output="A summary and a link to the most relevant page.",
        tools=[search_tool],
        agent=web_search_agent,
    )

    scraping_task = Task(
        description="Extract and summarize key insights from the given web page about '{topic}'.",
        expected_output="Detailed and concise insights from the page.",
        tools=[scrape_tool],
        agent=web_scraper_agent,
    )

    return Crew(
        agents=[web_search_agent, web_scraper_agent],
        tasks=[search_task, scraping_task],
        verbose=1,
        memory=False,
    )


def get_web_content(query):
    """Retrieve content via web scraping"""
    crew = setup_web_scraping_agent()
    result = crew.kickoff(inputs={"topic": query})
    return result.raw


# =========================
# Vector DB (PDF Processing)
# =========================

def setup_vector_db(file_path):
    """Create a FAISS vector database from a PDF"""
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_db = FAISS.from_documents(chunks, embeddings)

    return vector_db


def get_local_content(vector_db, query):
    """Search for relevant content in the local FAISS database"""
    docs = vector_db.similarity_search(query, k=5)
    return " ".join([doc.page_content for doc in docs])


# =========================
# LLM Response Generation
# =========================

def generate_final_answer(context, query):
    """Use LLM to generate final answer"""
    messages = [
        ("system", "You are a helpful assistant. Use only the provided context to answer."),
        ("system", f"Context: {context}"),
        ("human", query),
    ]

    response = llm.invoke(messages)
    if not response or not getattr(response, "content", None):
        raise ValueError("Invalid response from LLM.")
    return response.content


# =========================
# Main Query Processor
# =========================

def process_query(query, vector_db, local_context):
    """Main query pipeline"""
    print(f"Processing query: {query}")

    can_answer_locally = check_local_knowledge(query, local_context)
    print(f"Can answer locally: {can_answer_locally}")

    if can_answer_locally:
        context = get_local_content(vector_db, query)
    else:
        context = get_web_content(query)

    answer = generate_final_answer(context, query)
    return answer, "local" if can_answer_locally else "web"


# =========================
# CLI / Manual Test Entry
# =========================

def main():
    pdf_path = "genai-principles.pdf"
    print("Setting up vector DB...")
    vector_db = setup_vector_db(pdf_path)

    local_context = get_local_content(vector_db, "")
    query = "Summarize principles of generative AI"
    result = process_query(query, vector_db, local_context)
    print("\nFinal Answer:\n", result)


if __name__ == "__main__":
    main()
