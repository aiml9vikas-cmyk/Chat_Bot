import streamlit as st
from src.componants.ui.streamlit_ui.display_result import DisplayResultStreamlit
from src.componants.utils.audio_transcribe import transcribe_audio
from src.componants.ui.streamlit_ui.loadui import LoadStreamlitUI
from src.componants.llms.groqllm import GroqLLM
from src.componants.llms.openaillm import OpenAILLM
from src.componants.graph.graph_builder import GraphBuilder
from src.componants.ui.streamlit_ui.display_result import DisplayResultStreamlit

def load_llm(user_input):
    if user_input["selected_llm"] == "Groq":
        return GroqLLM(user_controls_input=user_input).get_llm_model()
    elif user_input["selected_llm"] == "OpenAI":
        return OpenAILLM(user_controls_input=user_input).get_llm_model()
    raise ValueError("Unsupported LLM selected.")


def main():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Replay chat history on every rerun.
    for m in st.session_state.messages:
        avatar = "🧑\u200d💻" if m["role"] == "user" else "🕸️"
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])

    if not st.session_state.messages:
        st.markdown(
            f"""
            <div style="text-align:center; padding: 60px 20px; opacity: 0.6;">
                <div style="font-size: 40px;">🕸️</div>
                <div style="font-size: 15px; margin-top: 8px;">
                    Usecase: <b>{user_input.get('selected_usecase')}</b> ·
                    Model: <b>{user_input.get('selected_model')}</b><br>
                    Send a message below to get started.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    voice_col = st.columns([1, 6, 1])[2]
    with voice_col:
        with st.popover("🎙️ Voice", use_container_width=True):
            st.caption("Record a message, then it's sent automatically.")
            audio_value = st.audio_input("Record", label_visibility="collapsed")

    user_message = st.chat_input("Enter your message...")

    # Transcribe mic input (only once per new recording) and treat it
    # exactly like a typed message.
    if audio_value is not None:
        audio_bytes = audio_value.getvalue()
        audio_hash = hash(audio_bytes)
        if st.session_state.get("last_audio_hash") != audio_hash:
            st.session_state["last_audio_hash"] = audio_hash
            provider = user_input.get("selected_llm")
            api_key = user_input.get("GROQ_API_KEY") or user_input.get("OPENAI_API_KEY")
            if not api_key:
                st.warning(f"Enter your {provider} API key in the sidebar to use voice input.")
            else:
                with st.spinner("Transcribing..."):
                    try:
                        user_message = transcribe_audio(audio_bytes, provider, api_key)
                    except Exception as e:
                        st.error(f"❌ Transcription failed: {e}")

    if user_message:
        try:
            model = load_llm(user_input)
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(user_input["selected_usecase"])

            DisplayResultStreamlit(
                usecase=user_input["selected_usecase"],
                graph=graph,
                user_message=user_message,
            ).display_result_on_ui()

        except Exception as e:
            st.error(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
