# Basic Chatbot

This project currently contains an early chatbot prototype built in `basic_chatbot.ipynb`.

## What has been done so far

- Set up a simple LangGraph flow with a single chat node.
- Used `ChatOllama` with `llama3.1:8b` as the local model.
- Defined a message-based state to carry conversation history.
- Added in-memory checkpointing with `MemorySaver`.
- Tested a terminal-style chat loop using a fixed `thread_id`.
- Verified that the bot can remember details from the same conversation thread.

## Current status

Right now, the chatbot works as a notebook-first experiment.  
It can take user input, respond, and keep short-term conversation memory inside the same thread.

One issue has already been identified:

- Calling the graph without the required checkpoint configuration raises an error.

## Project file

- `basic_chatbot.ipynb` - main development notebook for the chatbot prototype

## What comes next

The base is ready.  
The memory is awake.  
The next step is not just about making it answer better, but making it feel more alive.

More is coming.
