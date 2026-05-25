from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage , HumanMessage
# from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

# node definition
def chat_node(state:ChatState):

    # take user query from state
    message = state['messages']

    # send to llm
    response = llm.invoke(message)

    # add to messages
    return {'messages': [response]}

# DataBase
conn = sqlite3.connect(database='ChatbotDB.db',check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)


# graph construction
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)



 # STREAMING RESPONSE
# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content='create a blog on AI in 500 words')]},
#     config = {'thread_id': 'thread_1'},
#     stream_mode = 'messages'   
# ):

# # print(type(response))

#     if message_chunk.content:
#         print(message_chunk.content, end= " ", flush = True)



# test

# CONFIG = {'configurable': {'thread_id': 'thread-2'}}

# response = chatbot.invoke({
#         'messages': [HumanMessage(content='Hi my name is john, can you introduce yourself?')],
#     }, config = CONFIG
# )

# print(response['messages'][-1].content)

def retrieve_all_threads():
    all_threads =set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)
    