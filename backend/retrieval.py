import os
import json
import getpass
from dotenv import load_dotenv
from typing import List, Dict

# LangChain imports for the new architecture
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import Qdrant

# New chain components
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage # Explicitly import for clarity
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory # The in-memory history class
from langchain_core.chat_history import BaseChatMessageHistory # Import the base class for type hinting
from langchain_core.runnables import RunnablePassthrough, RunnableLambda # Import RunnableLambda for explicit output formatting

# --- 1. Load environment variables ---
load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Qdrant configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

# --- 2. RAG Setup (Qdrant and Embeddings) ---
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large", # Ensure this matches your Qdrant collection's dimension (3072)
    openai_api_key=OPENAI_API_KEY,
)

# Connect to your existing Qdrant collection
vectorstore = Qdrant.from_existing_collection(
    embedding=embeddings,
    url=QDRANT_URL,
    prefer_grpc=False,
    api_key=QDRANT_API_KEY,
    collection_name=QDRANT_COLLECTION_NAME,
)

# Create a retriever from the vectorstore
qdrant_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# --- 3. LLM Configuration ---
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.3)

# --- 4. Define prompts for the two main parts of the RAG chain ---

# A. Prompt for the history-aware retriever (to generate a standalone query)
history_aware_retriever_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("system", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only return the query itself."),
])

# B. Prompt for the document combining chain (to generate the final answer)
Youtube_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are UCA Chatbot, an expert academic assistant **strictly limited** to FST Marrakech.
     Your sole and **ABSOLUTE source of truth** is the context provided by searching FST Marrakech documents.
     Answer user questions *only* based on the information provided in the context below.
     If the requested information is **not** in the provided documents, or if the question is off-topic for FST Marrakech,
     respond clearly: "I am an FST Marrakech assistant, I cannot answer questions outside of this scope or find the requested information."
     Never provide general information, opinions, or answers based on your pre-trained knowledge.
     Always respond in French. For lists, use clear numbering.
     If greeted, respond with a greeting and ask how you can help, specifying your FST Marrakech role.
     
     Context: {context}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])


# --- 5. In-memory conversation history storage ---
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates an in-memory chat message history object for a given session ID.
    History is lost on script restart.
    """
    if session_id not in store:
        print(f"DEBUG: Creating new in-memory ChatMessageHistory for session: {session_id}")
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# --- 6. Create the RAG chain components and assemble them ---

# A. Create the history-aware retriever
history_aware_retriever = create_history_aware_retriever(
    llm, qdrant_retriever, history_aware_retriever_prompt
)

# B. Create the document combining chain
document_combiner_chain = create_stuff_documents_chain(llm, Youtube_prompt)

# C. Assemble the full RAG chain using RunnablePassthrough and RunnableLambda
# This ensures that the final output is always a dictionary with an 'answer' key.
rag_chain = (
    RunnablePassthrough.assign(
        context=history_aware_retriever, # Retrieves docs based on history-aware query
    )
    # The output of the previous step (which contains 'input', 'chat_history', and 'context')
    # is passed to document_combiner_chain. Its output is the raw LLM string.
    | document_combiner_chain
    # This RunnableLambda explicitly wraps the raw LLM string into a dictionary with 'answer' key
    | RunnableLambda(lambda x: {"answer": x})
)

# D. Wrap the full RAG chain with RunnableWithMessageHistory for session management
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer" # Explicitly tell RunnableWithMessageHistory where to find the AI's response
)

# --- 7. Main conversation loop function ---
def ask_uca_chatbot(user_query: str, session_id: str):
    print(f"\n--- User: {session_id} ---")
    print(f"User Query: {user_query}")

    try:
        response = conversational_rag_chain.invoke(
            {"input": user_query},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Now, response is guaranteed to be a dictionary with an 'answer' key
        assistant_response_text = response["answer"]
        
        print(f"UCA Chatbot: {assistant_response_text}")
        return assistant_response_text

    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        # import traceback; traceback.print_exc() # Uncomment for full traceback during debugging
        return "Désolé, une erreur inattendue est survenue. Veuillez réessayer."

# --- 8. Example Usage ---
if __name__ == "__main__":
    print("\nWelcome to the FST Marrakech UCA Chatbot (temporary session version)!")
    print("Type 'quitter' for a fresh start anytime, or 'quitter' to end the conversation.")

    current_user_session_id = "temp_user_session_abc123"

    # Initial greeting
    ask_uca_chatbot("Bonjour", current_user_session_id)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quitter':
            print("UCA Chatbot: Au revoir!")
            break

        ask_uca_chatbot(user_input, current_user_session_id)