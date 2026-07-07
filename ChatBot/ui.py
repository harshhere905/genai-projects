import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(page_title="Personality Chatbot", page_icon="🤖")

st.title("🤖 Personality Chatbot")
st.caption("Choose a personality and start chatting. Same logic as the CLI version, just with a UI.")

# Initialize model once
@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_tokens=500
    )

model = get_model()

# Session state to persist messages and behaviour across reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

if "behaviour_set" not in st.session_state:
    st.session_state.behaviour_set = False

# Sidebar for personality selection (only before chat starts, like the CLI input)
with st.sidebar:
    st.header("Setup")
    behaviour = st.selectbox(
        "Choose AI behaviour:",
        ["Angry", "Happy", "Sad", "Rude"],
        disabled=st.session_state.behaviour_set
    )

    if not st.session_state.behaviour_set:
        if st.button("Start Chat"):
            st.session_state.messages.append(
                SystemMessage(content=f"You are a {behaviour} AI. Respond accordingly.")
            )
            st.session_state.behaviour_set = True
            st.rerun()
    else:
        st.success(f"Personality set: **{behaviour}**")
        if st.button("Reset Chat"):
            st.session_state.messages = []
            st.session_state.behaviour_set = False
            st.rerun()

# Display chat history (skip the SystemMessage, it's not part of the visible conversation)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("human"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.markdown(msg.content)

# Chat input (only enabled after personality is chosen)
if st.session_state.behaviour_set:
    prompt = st.chat_input("Type your message...")

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("human"):
            st.markdown(prompt)

        with st.chat_message("ai"):
            with st.spinner("Thinking..."):
                response = model.invoke(st.session_state.messages)
                text = response.content
                st.markdown(text)

        st.session_state.messages.append(AIMessage(content=text))
else:
    st.info("👈 Choose a personality and click **Start Chat** in the sidebar to begin.")