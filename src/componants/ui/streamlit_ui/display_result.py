import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

USER_AVATAR = "🧑\u200d💻"
AI_AVATAR = "🕸️"


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        # Show the user's new message immediately.
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(self.user_message)
        st.session_state.messages.append({"role": "user", "content": self.user_message})

        with st.chat_message("assistant", avatar=AI_AVATAR):
            placeholder = st.empty()
            full_response = ""
            tool_calls_seen = []

            history = self._history_as_lc_messages()

            with st.spinner("Thinking...", show_time=True):
                for event in self.graph.stream({"messages": history}):
                    for node_name, value in event.items():
                        for msg in value.get("messages", []):
                            if isinstance(msg, AIMessage) and msg.content:
                                full_response = msg.content
                                placeholder.markdown(full_response)
                            elif isinstance(msg, ToolMessage):
                                tool_calls_seen.append(node_name)

            if tool_calls_seen:
                with st.expander("🔧 Tool calls used", expanded=False):
                    for t in tool_calls_seen:
                        st.write(f"• {t}")

            if not full_response:
                full_response = "_(no response generated)_"
                placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    def _history_as_lc_messages(self):
        lc_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                lc_messages.append(HumanMessage(content=m["content"]))
            else:
                lc_messages.append(AIMessage(content=m["content"]))
        lc_messages.append(HumanMessage(content=self.user_message))
        return lc_messages
