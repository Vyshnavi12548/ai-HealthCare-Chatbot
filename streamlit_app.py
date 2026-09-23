import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="AI Healthcare Assistant",
    page_icon="💬",
    layout="centered"
)

# Title and description
st.title("💬 AI Healthcare Assistant")

st.write(
    "This AI assistant provides general health information for educational purposes. "
    "It is not a substitute for professional medical advice."
)

# Get Gemini API key from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Create Gemini client
client = genai.Client(api_key=api_key)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you?"):

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Gemini response
    with st.chat_message("assistant"):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            answer = response.text
            st.markdown(answer)

            # Save assistant response
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(
                "The AI service is temporarily unavailable. "
                "Please try again in a moment."
            )