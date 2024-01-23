from openai import OpenAI
import streamlit as st
import base64

LOGO_IMAGE = "colab.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .logo-text1 {
        margin-left: 10px;
        font-weight:700 !important;
        font-size:60px !important;
        color: #000000  !important;
        padding-top: 75px !important;
    }
    .logo-text2 {
        margin-left: 0px;
        font-weight:700 !important;
        font-size:60px !important;
        color: #5f97bf!important;
        padding-top: 75px !important;
    }
    .logo-img {
        margin-top: 61px;
        float:right;
        width: 100px;
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text1">CO-LAB&nbsp</p>
        <p class="logo-text2">CO-PILOT</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: block;
        background-image: linear-gradient(90deg, rgb(0, 102, 204), rgb(102, 255, 255));
        position: absolute;
        top: 0px;
        right: 0px;
        left: 0px;
        height: 0.250rem;
	}
            
    [data-testid="stChatInput"]{
            
        background-color: rgba(0, 0, 0, 0);
            
        border-bottom-color: rgba(46,81,115,255);
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        border-bottom-style: solid;
        border-bottom-width: 2px;
            
        border-left-color: rgba(46,81,115,255);
        border-left-style: solid;
        border-left-width: 2px;
            
        border-right-color: rgba(46,81,115,255);
        border-right-style: solid;
        border-right-width: 2px;
            
        border-top-color: rgba(46,81,115,255);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-top-style: solid;
        border-top-width: 2px;
            
        box-sizing: border-box; 
    }
            
    [data-testid="stChatMessage"]{
            
        background-color: rgba(255, 255, 255, 0.45);
        box-sizing: border-box; 
        border-top-color: rgba(0, 0, 0, 0);
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-top-style: solid;
        border-top-width: 2px;
            
    }

</style>""",

unsafe_allow_html=True)

# Initialize OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Check if the openai_model is not set in the session state, set it to the default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Check if 'messages' are not in the session state, initialize it as an empty list
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from the session state
user = "person-fill.svg"
assistant = "blue-bot.svg"

# Check if the role is "user" or "assistant" to set the appropriate avatar. 
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar=user):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar=assistant):
            st.markdown(message["content"])

# Get user input from the chat input box
if prompt := st.chat_input("Ask a question..."):
    # Add user input to session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user input as a chat message
    with st.chat_message("user", avatar=user):
        st.markdown(prompt)

    # Use OpenAI API to generate assistant's response
    with st.chat_message("assistant", avatar=assistant):
        message_placeholder = st.empty()
        full_response = "&nbsp;&nbsp;" #add some white space before the bot responds
        
        # Iterate over OpenAI completions (streaming mode)
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")  # Display response with a streaming effect
        message_placeholder.markdown(full_response)  # Display the final response
    st.session_state.messages.append({"role": "assistant", "content": full_response})  # Add assistant's response to session state