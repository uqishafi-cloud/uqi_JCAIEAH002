import os
from dotenv import load_dotenv, find_dotenv

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

load_dotenv(find_dotenv())

lf = Langfuse()
langfuse_handler = CallbackHandler()

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

def get_vector_store():
    """Mengambil instance Vector Store menggunakan client global."""
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        embedding=embeddings,
    )

def get_system_prompt():
    """
    Mencoba mengambil prompt 'hr_supervisor' dari Langfuse Cloud.
    Jika belum dibuat di Cloud, gunakan Default Prompt (Fallback).
    """
    try:
        # Coba tarik prompt dari Langfuse
        prompt = lf.get_prompt("hr_supervisor")
        return prompt.get_langchain_prompt()
    except Exception:
        # Fallback Prompt (Jika di cloud belum setup)
        print("Prompt 'hr_supervisor' tidak ditemukan di Langfuse. Menggunakan Default.")
        return ChatPromptTemplate.from_messages([
            ("system", """
             Anda adalah HR Assistant Professional & Supervisor.
             Tugas anda adalah membantu user mencari kandidat, menghitung gaji, dan membuat soal interview.
             
             ATURAN KEAMANAN (RBAC):
             - Anda wajib tahu Role User saat ini: '{current_role}'
             - Jika User adalah 'Intern' atau 'Staff', mereka DILARANG melihat data resume atau gaji.
             - Gunakan tool yang sesuai dengan permintaan user.
             """),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

@tool
def search_resume(query: str, user_role: str):
    """
    Gunakan tool ini untuk MENCARI KANDIDAT atau RESUME dari database.
    Wajib menyertakan 'query' dan 'user_role'.
    """
    # 1. Security Check
    allowed_roles = ["hr", "manager", "admin", "vp"]
    if user_role.lower().strip() not in allowed_roles:
        return "AKSES DITOLAK: Maaf, role Anda tidak memiliki izin untuk melihat data resume kandidat."

    # 2. Logic Pencarian
    try:
        vector_store = get_vector_store()
        docs = vector_store.similarity_search(query, k=5)
        
        if not docs:
            return "Tidak ditemukan kandidat yang cocok."
            
        results = []
        for idx, doc in enumerate(docs):
            info = f"Kandidat #{idx+1} (ID: {doc.metadata.get('ID', 'N/A')}): {doc.page_content[:500]}..."
            results.append(info)
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"Terjadi kesalahan pada database Qdrant: {e}"
    
@tool
def search_by_skill(skill_query: str):
    """
    Gunakan tool ini KHUSUS untuk mencari kandidat berdasarkan SKILL TEKNIS / HARD SKILL.
    Contoh: "Kandidat yang jago Python", "Bisa SQL dan Tableau", "Skill Analysis".
    """
    try:
        store = get_vector_store()
        docs = store.similarity_search(skill_query, k=5)
        
        results = []
        for idx, doc in enumerate(docs):
            info = f"""
            Kandidat #{idx+1} [ID: {doc.metadata.get('ID', 'N/A')}]
            Category: {doc.metadata.get('Category', 'N/A')}
            Cuplikan Resume: {doc.page_content[:600]}...
            """
            results.append(info)
            
        return "\n".join(results)
    except Exception as e: return f"Error DB: {e}"

@tool
def estimasi_gaji(experience_year: int, role_target: str, user_role: str):
    """
    Gunakan tool ini untuk MENGHITUNG ESTIMASI GAJI (Salary Range).
    Hanya untuk HR/Manager.
    """
    if user_role.lower().strip() not in ["hr", "manager", "admin"]:
        return "MAAF: Informasi sensitif mengenai gaji hanya dapat diakses oleh HR atau Manager."

    try:
        base_salary = 5_000_000
        exp_multiplier = 1_500_000
        
        role_bonus = 0
        if "manager" in role_target.lower(): role_bonus = 10_000_000
        elif "lead" in role_target.lower(): role_bonus = 5_000_000
        elif "senior" in role_target.lower(): role_bonus = 3_000_000
        
        est_bawah = base_salary + (experience_year * exp_multiplier) + role_bonus
        est_atas = est_bawah * 1.3 # Range 30%
        
        return f"Kalkulasi Sistem untuk {role_target} ({experience_year} thn): Rp {est_bawah:,.0f} - Rp {est_atas:,.0f}"
    except Exception as e:
        return f"Error kalkulasi: {e}"

@tool
def generate_pertanyaan_interview(skill_fokus: str, level: str):
    """
    Gunakan tool ini untuk MEMBUAT PERTANYAAN INTERVIEW dan KUNCI JAWABAN.
    Bisa diakses oleh semua role.
    """
    return f"""
    INSTRUKSI SISTEM UNTUK LLM:
    User meminta soal interview untuk skill: {skill_fokus} dengan level: {level}.
    Buatkan 3 pertanyaan teknis yang mendalam (tricky) beserta poin-poin jawaban yang diharapkan.
    """

# --- AGENT EXECUTOR FACTORY ---

def get_agent_executor():
    """
    Fungsi utama yang dipanggil oleh app.py untuk menjalankan Agent.
    """
    tools = [search_resume, estimasi_gaji, generate_pertanyaan_interview]
    
    prompt = get_system_prompt()
    
    agent = create_tool_calling_agent(model, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)