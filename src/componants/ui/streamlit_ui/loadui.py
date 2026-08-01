import os
import streamlit as st
from src.componants.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title="🕸️ LangGraph Agentic AI",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        self._inject_css()

        st.markdown(
            """
            <div class="app-header">
                <span class="app-header-icon">🕸️</span>
                <div>
                    <div class="app-header-title">LangGraph: Build Stateful Agentic AI graph</div>
                    <div class="app-header-subtitle">Configure your agent in the sidebar, then start chatting</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.sidebar:
            st.markdown('<div class="sidebar-brand">⚙️ Agent Settings</div>', unsafe_allow_html=True)

            # --- LLM selection ---
            llm_options = self.config.get_llm_options()
            selected_llm = st.selectbox("Select LLM", llm_options, key="selected_llm")
            self.user_controls["selected_llm"] = selected_llm

            # --- Model selection ---
            model_options = self.config.get_model_options(selected_llm)
            selected_model = st.selectbox("Select Model", model_options, key="selected_model")
            self.user_controls["selected_model"] = selected_model

            # --- API key(s) ---
            st.markdown('<div class="sidebar-section-label">API Key</div>', unsafe_allow_html=True)
            if selected_llm == "Groq":
                groq_key = st.text_input(
                    "Groq API Key", type="password",
                    value=os.environ.get("GROQ_API_KEY", ""),
                    label_visibility="collapsed",
                )
                self.user_controls["GROQ_API_KEY"] = groq_key
                if not groq_key:
                    st.warning("⚠️ Please enter your Groq API key.", icon="🔑")
            elif selected_llm == "OpenAI":
                openai_key = st.text_input(
                    "OpenAI API Key", type="password",
                    value=os.environ.get("OPENAI_API_KEY", ""),
                    label_visibility="collapsed",
                )
                self.user_controls["OPENAI_API_KEY"] = openai_key
                if not openai_key:
                    st.warning("⚠️ Please enter your OpenAI API key.", icon="🔑")

            # --- Usecase selection ---
            usecase_options = self.config.get_usecase_options()
            selected_usecase = st.selectbox("Select Usecase", usecase_options, key="selected_usecase")
            self.user_controls["selected_usecase"] = selected_usecase

            # --- Extra keys some usecases need ---
            for extra_key in self.config.get_extra_keys_for_usecase(selected_usecase):
                val = st.text_input(
                    extra_key.replace("_", " ").title(),
                    type="password",
                    value=os.environ.get(extra_key, ""),
                )
                self.user_controls[extra_key] = val
                if not val:
                    st.warning(f"⚠️ Please enter your {extra_key.replace('_', ' ').title()}.", icon="🔑")

            st.divider()
            if st.button("🧹 Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

            st.markdown(
                '<div class="sidebar-footer">Built with LangGraph + Streamlit</div>',
                unsafe_allow_html=True,
            )

        return self.user_controls

    def _inject_css(self):
        st.markdown(
            """
            <style>
            .app-header {
                display: flex; align-items: center; gap: 14px;
                padding: 18px 22px; margin-bottom: 18px;
                border-radius: 14px;
                background: linear-gradient(135deg, #507A98 0%, #111827 100%);
                color: #fff;
            }
            .app-header-icon { font-size: 34px; }
            .app-header-title { font-size: 22px; font-weight: 700; }
            .app-header-subtitle { font-size: 13px; opacity: 0.75; margin-top: 2px; }

            .sidebar-brand {
                font-size: 16px; font-weight: 700; margin-bottom: 10px;
                padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .sidebar-section-label {
                font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em;
                opacity: 0.6; margin-top: 4px; margin-bottom: -6px;
            }
            .sidebar-footer {
                font-size: 11px; opacity: 0.5; text-align: center; margin-top: 18px;
            }

            [data-testid="stChatMessage"] {
                border-radius: 14px; padding: 4px 2px;
            }

            .stButton>button {
                border-radius: 10px; font-weight: 600;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
