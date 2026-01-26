import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from langfuse.langchain import CallbackHandler 

from modules.auth import authenticate 
from modules.agent import supervisor_agent as agent

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="HR Agent System", page_icon="🔐", layout="centered")

st.markdown("""
<style>
    .stChatMessage { margin-bottom: 10px; }
    div[data-testid="stToast"] { display: none; }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    
if "messages" not in st.session_state:
    st.session_state["messages"] = []

#--------- LOGIN ---------
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align: center;'>🔐 Smart HR Assistant</h1>", unsafe_allow_html=True)
    
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
                    st.rerun()
                else:
                    st.error("❌ Username atau Password salah!")
    
    with st.expander("ℹ️ Info Akun Demo"):
        st.markdown("""
        - **HR:** `uqi` / `admin`
        - **Intern:** `herman` / `123`
        """)

#---------HALAMAN UTAMA ---------
else:
    curr_user = st.session_state["user_info"]
    user_name = curr_user['name']
    user_role = curr_user['role']

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("User Profile")
        st.write(f"👤 {user_name}")
        st.info(f"🏷️ **Role:** {user_role}")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user_info"] = None
            st.session_state["messages"] = []
            st.rerun()

    # --- HEADER ---
    st.title("🤖 Smart HR Assistant")
    st.caption(f"Logged in as **{user_role}**.")

    # --- DISPLAY HISTORY ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- INPUT USER ---
    if prompt := st.chat_input("Ketik perintah Anda..."):
        
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # SIAPKAN PAYLOAD
        history_buffer = []
        for m in st.session_state.messages[-10:]:
            if m["role"] == "user":
                history_buffer.append(HumanMessage(content=m["content"]))
            else:
                history_buffer.append(AIMessage(content=m["content"]))

        final_prompt = f"{prompt}\n\n[SYSTEM INFO: Current User Role is '{user_role}']"
        input_payload = {"messages": history_buffer + [HumanMessage(content=final_prompt)]}

        # PROSES DI BACKEND
        with st.chat_message("assistant"):
            with st.spinner("Sedang memproses..."):
                try:
                    lf_handler = CallbackHandler(session_id=f"sess-{user_name}", user_id=user_name)
                    
                    result = agent.invoke(
                        input_payload,
                        config={"callbacks": [lf_handler]} 
                    )
                    
                    # --- EXTRAK DATA ---
                    answer = result["messages"][-1].content
                    
                    total_input_tokens = 0
                    total_output_tokens = 0
                    tool_calls_view = []

                    for message in result["messages"]:
                        # Ambil Metadata Token
                        if hasattr(message, "response_metadata"):
                            meta = message.response_metadata
                            if "token_usage" in meta:
                                total_input_tokens += meta["token_usage"].get("prompt_tokens", 0)
                                total_output_tokens += meta["token_usage"].get("completion_tokens", 0)
                            elif "usage_metadata" in meta:
                                total_input_tokens += meta["usage_metadata"].get("input_tokens", 0)
                                total_output_tokens += meta["usage_metadata"].get("output_tokens", 0)
                        
                        if isinstance(message, ToolMessage):
                            tool_calls_view.append(f"🔧 Tool Output: {message.content}")

                    price = 17_000 * (total_input_tokens * 0.15 + total_output_tokens * 0.6) / 1_000_000

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    with st.expander("📊 Statistik & Debug"):
                        st.write(f"**Estimasi Biaya:** Rp {price:,.2f}")
                        st.write(f"**Tokens:** Input ({total_input_tokens}) + Output ({total_output_tokens})")
                        if tool_calls_view:
                            st.divider()
                            for t in tool_calls_view:
                                st.code(t)

                except Exception as e:
                    st.error(f"Terjadi kesalahan sistem: {e}")