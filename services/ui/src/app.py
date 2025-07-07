# from streamlit import config
# config.set_option("browser.gatherUsageStats", False)

# import streamlit as st
# from utils.api_client import post_agentic_query
# from utils.logger import setup_logger

# logger = setup_logger()

# # Page Configuration
# st.set_page_config(
#     page_title="LangChain MCP Demo UI",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.title("🤖 LangChain MCP Demo UI")

# # Session State Setup
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Chat History Display
# with st.container():
#     st.markdown("### 💬 Conversation")
#     for chat in st.session_state.chat_history:
#         with st.chat_message("user"):
#             st.markdown(chat["user"])
#         with st.chat_message("assistant"):
#             st.markdown(chat["bot"])

# # Divider
# st.markdown("---")

# # Input Form (Enter to Submit + Button UI)
# with st.form(key="chat_form", clear_on_submit=True):
#     user_input = st.text_input("Your message:", placeholder="Ask your question here...", key="user_input", label_visibility="collapsed")
#     submit_button = st.form_submit_button(label="Send 🚀")

#     if submit_button and user_input.strip():
#         with st.spinner("Thinking..."):
#             result = post_agentic_query(user_input)

#         if result["status"] == "success":
#             answer = result["content"].get("content", "No response.")
#             st.session_state.chat_history.append({"user": user_input, "bot": answer})
#             st.rerun()
#         else:
#             st.error(f"❌ {result['content']}")

# # Reset Chat Option
# with st.sidebar:
#     if st.button("🧹 Clear Chat History"):
#         st.session_state.chat_history.clear()
#         st.success("Chat history cleared.")
#         st.rerun()
