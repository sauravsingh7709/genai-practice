# flake8: noqa
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver  
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    #messages ko add karega jab tak mera graph invoke nhi karega ,
    #jab graph invoke hoga tab pichla state jo hai remove ho jaayega 
    #lets say multiple nodes hai , graph unn sab ko chalyega , so annotated jo hai message mein information add karega 
    #jiise ki ek node ko dusre ka refernce mil sake , means tab tak llm ke pass memeory hai , jaise hi invoke hua naya state 
    #bnn jaayega 
    messages: Annotated[list, add_messages]

# ye jaise hum openai ka sdk use karte hain waise hi langchain ka chat model use karenge
llm = ChatOpenAI(model="gpt-4.1-nano")

def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer

def chat_node(state: State):
    response = llm.invoke(state["messages"])
    #
    return {"messages": [response]}

graph_builder = StateGraph(State)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

graph=graph_builder.compile()

def main():
    
    #   mongodb://<username>:<pass>@<host>:<port>
    DB_URI = "mongodb://admin:admin@mongodb:27017"
    config = {"configurable": {"thread_id": "3"}}
    
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_mongo=compile_graph_with_checkpointer(mongo_checkpointer)
        
        query = input("> ")
        result = graph_with_mongo.invoke({"messages": [{"role": "user", "content": query}]},config)
        print(result)
    

main()