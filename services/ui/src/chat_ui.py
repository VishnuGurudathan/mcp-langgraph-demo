"""
LangChain MCP Demo Chat UI

This module provides a Streamlit-based chat interface for interacting with the 
MCP (Model Context Protocol) LangGraph demonstration platform. It handles user
interactions, conversation history, and communication with the backend services.

Features:
- Real-time chat interface with conversation history
- Error handling and user feedback
- Session state management
- Responsive UI with proper styling

Author: MCP LangGraph Demo Team
Version: 1.0.0
"""

from streamlit import config
config.set_option("browser.gatherUsageStats", False)

import streamlit as st
from typing import Dict, Any, List, Optional
import traceback

from utils.api_client import post_agentic_query
from utils.logger import setup_logger
from utils.ui_helpers import inject_custom_css

# Initialize logger for this module
logger = setup_logger(__name__)

# ============================================
# CONFIGURATION & CONSTANTS
# ============================================

# Page configuration constants
PAGE_CONFIG = {
    "page_title": "LangChain MCP Demo UI",
    "layout": "centered",
    "initial_sidebar_state": "collapsed"
}

# UI text constants
UI_TEXT = {
    "title": "🤖 LangChain MCP Demo UI",
    "conversation_header": "💬 Conversation",
    "input_placeholder": "Ask your question here...",
    "send_button": "Send 🚀",
    "clear_button": "🧹 Clear Chat History",
    "thinking_message": "Thinking...",
    "clear_success": "Chat history cleared.",
    "error_prefix": "❌"
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

def initialize_session_state() -> None:
    """
    Initialize session state variables for the chat application.
    
    This function ensures that required session state variables exist
    with appropriate default values.
    """
    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            logger.info("Initialized chat history in session state")
    except Exception as e:
        logger.error(f"Error initializing session state: {str(e)}")
        st.error("Failed to initialize application state")


def validate_user_input(user_input: str) -> bool:
    """
    Validate user input before processing.
    
    Args:
        user_input (str): The user's input message
        
    Returns:
        bool: True if input is valid, False otherwise
    """
    try:
        # Check if input is not empty and not just whitespace
        if not user_input or not user_input.strip():
            logger.warning("Empty or whitespace-only user input received")
            return False
            
        # Check input length (reasonable limits)
        if len(user_input.strip()) > 1000:
            logger.warning(f"User input too long: {len(user_input)} characters")
            st.warning("Message too long. Please keep it under 1000 characters.")
            return False
            
        logger.debug(f"User input validated successfully: {len(user_input)} characters")
        return True
        
    except Exception as e:
        logger.error(f"Error validating user input: {str(e)}")
        return False


def process_user_query(user_input: str) -> Dict[str, Any]:
    """
    Process user query and handle API communication.
    
    Args:
        user_input (str): The user's input message
        
    Returns:
        Dict[str, Any]: Result dictionary with status and content
    """
    try:
        logger.info(f"Processing user query: '{user_input[:50]}{'...' if len(user_input) > 50 else ''}'")
        
        # Make API call to backend
        result = post_agentic_query(user_input)
        
        if result.get("status") == "success":
            logger.info("Query processed successfully")
            return result
        else:
            logger.warning(f"Query processing failed: {result.get('content', 'Unknown error')}")
            return result
            
    except Exception as e:
        logger.error(f"Error processing user query: {str(e)}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")
        return {
            "status": "error",
            "content": "An unexpected error occurred while processing your request."
        }


def add_to_chat_history(user_input: str, bot_response: str) -> None:
    """
    Add a conversation pair to the chat history.
    
    Args:
        user_input (str): The user's input message
        bot_response (str): The bot's response message
    """
    try:
        chat_entry = {"user": user_input, "bot": bot_response}
        st.session_state.chat_history.append(chat_entry)
        logger.info(f"Added chat entry to history. Total entries: {len(st.session_state.chat_history)}")
        
    except Exception as e:
        logger.error(f"Error adding to chat history: {str(e)}")
        st.error("Failed to save conversation to history")


def clear_chat_history() -> None:
    """
    Clear the chat history and provide user feedback.
    """
    try:
        history_length = len(st.session_state.chat_history)
        st.session_state.chat_history.clear()
        logger.info(f"Cleared chat history ({history_length} entries)")
        st.success(UI_TEXT["clear_success"])
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        st.error("Failed to clear chat history")


def render_chat_history() -> None:
    """
    Render the chat history in the UI.
    
    This function displays all previous conversation exchanges
    in a structured format with proper message attribution.
    """
    try:
        with st.container(height=450, border= False):
            #st.markdown(UI_TEXT["conversation_header"])
            
            # Display each conversation pair
            for i, chat in enumerate(st.session_state.chat_history):
                try:
                    # User message
                    with st.chat_message("user"):
                        st.markdown(chat.get("user", "No message"))
                    
                    # Assistant message
                    with st.chat_message("assistant"):
                        st.markdown(chat.get("bot", "No response"))
                        
                except Exception as e:
                    logger.error(f"Error rendering chat entry {i}: {str(e)}")
                    # Continue rendering other messages even if one fails
                    continue
                    
    except Exception as e:
        logger.error(f"Error rendering chat history: {str(e)}")
        st.error("Failed to display chat history")


def render_input_form() -> Optional[str]:
    """
    Render the user input form and handle submission.
    
    Returns:
        Optional[str]: User input if submitted and valid, None otherwise
    """
    try:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Your message:", 
                placeholder=UI_TEXT["input_placeholder"], 
                key="user_input", 
                label_visibility="collapsed"
            )
            submit_button = st.form_submit_button(label=UI_TEXT["send_button"])

            # Handle form submission
            if submit_button:
                if validate_user_input(user_input):
                    return user_input.strip()
                else:
                    return None
                    
        return None
        
    except Exception as e:
        logger.error(f"Error rendering input form: {str(e)}")
        st.error("Failed to render input form")
        return None


def render_sidebar() -> None:
    """
    Render the sidebar with additional controls.
    """
    try:
        with st.sidebar:
            if st.button(UI_TEXT["clear_button"]):
                clear_chat_history()
                st.rerun()
                
    except Exception as e:
        logger.error(f"Error rendering sidebar: {str(e)}")


# ============================================
# MAIN APPLICATION
# ============================================

def main() -> None:
    """
    Main application function that orchestrates the LangChain MCP Demo chat UI.
    
    This function handles:
    - Streamlit page configuration
    - Custom CSS injection for layout
    - Chat session state initialization
    - Header rendering (fixed)
    - Chat history rendering (scrollable middle)
    - Input rendering (fixed at bottom using st.chat_input)
    - Message submission via Enter key
    - Response processing and error handling
    """
    try:
        logger.info("🚀 Starting LangChain MCP Demo UI application")

        # Page configuration (set page title, layout, etc.)
        st.set_page_config(**PAGE_CONFIG)
        logger.debug("✅ Page configuration set successfully")

        # Inject custom CSS for layout styling
        inject_custom_css()
        logger.debug("✅ Custom CSS injected")

        # Initialize session state (chat history, etc.)
        initialize_session_state()

        # --------------------------------------------
        # Render Fixed Header
        # --------------------------------------------
        st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="header-title">{UI_TEXT['title']}</div>
            <div class="header-subtitle">{UI_TEXT['conversation_header']}</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------------------------
        # Render Scrollable Chat History
        # --------------------------------------------
        st.markdown('<div class="responsive-chat-container " id="chat-box">', unsafe_allow_html=True)
        render_chat_history()
        st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------------------------
        # Render Fixed Input Footer
        # --------------------------------------------
        st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
        user_input = st.chat_input(UI_TEXT["input_placeholder"])
        st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------------------------
        # Handle User Query Submission
        # --------------------------------------------
        if user_input:
            logger.info(f"📨 Received user input: {user_input}")
            
            if validate_user_input(user_input):
                with st.spinner(UI_TEXT["thinking_message"]):
                    result = process_user_query(user_input)

                if result.get("status") == "success":
                    try:
                        answer = result.get("content", {}).get("content", "No response.")
                        add_to_chat_history(user_input, answer)
                        logger.info("✅ Response added to chat history")
                        st.rerun()  # Refresh to render new message
                    except Exception as e:
                        logger.error(f"⚠️ Failed to handle response: {str(e)}")
                        st.error("An error occurred while processing the response.")
                else:
                    error_message = result.get("content", "Unknown error occurred")
                    st.error(f"{UI_TEXT['error_prefix']} {error_message}")
                    logger.warning(f"Displayed error to user: {error_message}")
            else:
                logger.warning("User input validation failed")

        # --------------------------------------------
        # Sidebar: Clear Chat Option
        # --------------------------------------------
        render_sidebar()

        logger.debug("Chat UI rendering completed successfully")

    except Exception as e:
        logger.critical(f"Critical error in main application: {str(e)}")
        logger.debug(f"Full traceback: {traceback.format_exc()}")
        st.error("A critical error occurred. Please refresh the page and try again.")

# ============================================
# APPLICATION ENTRY POINT
# ============================================

if __name__ == "__main__":
    # Run the main application
    main()
