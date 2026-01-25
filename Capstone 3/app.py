import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.langchain import CallbackHandler

from modules.auth import authenticate
from modules.agent import supervisor_agent as agent

st.set_page_config(page_title="HR Agent System", page_icon="🔐", layout="centered")

st.markdown("""
<style>
    .stChatMessage { margin-bottom: 10px; }
    div[data-testid="stToast"] { display: none; }
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None # Menyimpan data user (Role, Nama)
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [] # Menyimpan history chat tampilan UI

# ==========================================
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center;'>🔐 HR System Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Silakan masuk untuk mengakses data kandidat.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Masuk Sistem", use_container_width=True)
            
            if submit:
                user = authenticate(username, password)
                
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = user
                    st.success(f"Login Berhasil! Halo, {user['name']}")
                    st.rerun() # Refresh halaman untuk masuk ke menu utama
                else:
                    st.error("Username atau Password salah!")
    
    with st.expander("ℹ️ Info Akun Demo"):
        st.markdown("""
        - **HR Manager:** `uqi` / `admin` (Akses Penuh)
        - **Intern/Magang:** `herman` / `123` (Akses Terbatas - Tidak bisa lihat Resume/Gaji)
        """)

# ==========================================
# Chatbot

else:
    # Ambil data user yang sedang login
    curr_user = st.session_state["user_info"]
    user_name = curr_user['name']
    user_role = curr_user['role']

    # --- SIDEBAR (Profil & Logout) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.title("User Profile")
        st.write(f"**Nama:** {user_name}")
        st.info(f"**Role:** {user_role}")
        
        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            # Reset semua state
            st.session_state["authenticated"] = False
            st.session_state["user_info"] = None
            st.session_state["messages"] = []
            st.rerun()

    st.title("Smart HR Assistant")
    st.caption(f"Logged in as **{user_role}**. Security Policy Applied.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ketik perintah Anda (Contoh: Cari kandidat Java)..."):
        

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- LOGIC PENGHUBUNG KE BACKEND ---
        
        # A. Siapkan History untuk Agent (Format LangChain)
        # Ambil 10 chat terakhir agar hemat token & memori
        history_buffer = []
        for m in st.session_state.messages[-10:]:
            if m["role"] == "user":
                history_buffer.append(HumanMessage(content=m["content"]))
            else:
                history_buffer.append(AIMessage(content=m["content"]))

        # B. Context Injection
        # Selipkan informasi role user ke dalam prompt
        final_prompt = f"{prompt}\n\n[SYSTEM INFO: Current User Role is '{user_role}']"
        
        # Gabungkan history + pesan baru
        input_payload = {"messages": history_buffer + [HumanMessage(content=final_prompt)]}

        # C. Kirim ke Agent Backend
        with st.chat_message("assistant"):
            with st.spinner("Sedang memproses..."):
                try:
                    # Setup Langfuse Tracking (Opsional, biar tercatat di dashboard)
                    lf_handler = CallbackHandler(
                        session_id=f"session-{user_name}",
                        user_id=user_name
                    )

                    # Panggil Agent!
                    response = agent.invoke(
                        input_payload,
                        config={"callbacks": [lf_handler]}
                    )
                    
                    # Ambil jawaban terakhir dari list messages (Gaya LangGraph)
                    ai_answer = response["messages"][-1].content
                    
                    # Tampilkan & Simpan
                    st.markdown(ai_answer)
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})

                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")