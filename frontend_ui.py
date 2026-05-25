import streamlit as st
from basic_chatbot import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


# *********************************************** UTILITY FUNCTIONS ***********************************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config = {'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])


# *********************************************** SESSION SETUP ***********************************************
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# *********************************************** SIDE BAR UI ************************************************

st.sidebar.title('Axon')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Conversations')

# showing the title for conversations in sidebar instead of thread id, we can show the first human message of the conversation as title
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(f'Chat {thread_id}'):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        top_message = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role ='user'
            else:
                role = 'assistant'
            top_message.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = top_message


# *********************************************** MAIN UI ************************************************
# printing the messages in list
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
# session_state -> dict -> 

user_input = st.chat_input('Type here...')

if user_input:
    # first add the message to the history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    

    # Invoke 
    # response = chatbot.invoke({'messages': HumanMessage(content = user_input)}, config=CONFIG)
    # ai_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)


    # STREAMING RESPONSE
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': HumanMessage(content=user_input)},
                config = CONFIG,
                stream_mode = 'messages'
            )
        )
    
    # append to session
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})