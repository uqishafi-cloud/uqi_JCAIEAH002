import os
from dotenv import load_dotenv, find_dotenv

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.agents import create_agent

from langfuse import Langfuse

load_dotenv(find_dotenv())
lf = Langfuse() 

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

model = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

# --- HELPER ---
def get_vector_store():
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embedding=embeddings,
    )

def get_system_prompt_template():
    try:
        prompt = lf.get_prompt("hr_supervisor")
        return prompt.get_langchain_prompt().messages[0].prompt.template
    except Exception:
        return "Anda adalah HR Assistant... (Default)"

# --- TOOLS ---

@tool
def search_resume(query: str, user_role: str):
    """Mencari kandidat berdasarkan POSISI/JABATAN."""
    if user_role.lower().strip() not in ["hr", "manager"]:
        return "AKSES DITOLAK. Informasi hanya untuk HR/Manager"
    try:
        store = get_vector_store()
        docs = store.similarity_search(query, k=5)
        return "\n".join([f"Kandidat (ID-{d.metadata.get('ID')}): {d.page_content[:500]}..." for d in docs])
    except Exception as e: return f"Error DB: {e}"

@tool
def search_by_skill(skill_query: str, user_role: str):
    """Mencari kandidat berdasarkan SKILL TEKNIS."""
    if user_role.lower().strip() not in ["hr", "manager"]:
        return "AKSES DITOLAK. Informasi hanya untuk HR/Manager"
    try:
        store = get_vector_store()
        docs = store.similarity_search(skill_query, k=5)
        return "\n".join([f"Skill Match (ID-{d.metadata.get('ID')}): {d.page_content[:500]}..." for d in docs])
    except Exception as e: return f"Error DB: {e}"

@tool
def estimasi_gaji(experience_year: int, role_target: str, user_role: str):
    """Menghitung estimasi gaji."""
    if user_role.lower().strip() not in ["hr", "manager"]:
        return "AKSES DITOLAK. Informasi hanya untuk HR/Manager"
    try:
        base = 5_000_000 + (experience_year * 1_500_000)
        return f"Estimasi: Rp {base:,.0f}"
    except Exception as e: return f"Error: {e}"

@tool
def generate_pertanyaan_interview(skill_fokus: str, level: str):
    """Membuat pertanyaan interview (Akses Publik)."""
    return f"Buatkan 3 pertanyaan interview tricky untuk skill {skill_fokus} level {level}."


# --- INIT ---
tools_list = [search_resume, search_by_skill, estimasi_gaji, generate_pertanyaan_interview]
lf_supervisor = get_system_prompt_template()

supervisor_agent = create_agent(
    model=model,
    tools=tools_list,
    system_prompt=lf_supervisor
)