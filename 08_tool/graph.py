from json import tool

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
import requests
from langchain_core.tools import tool
load_dotenv()

todos = []


@tool()
def add_todo(task: str):
    """Adds the input task to the DB"""
    todos.append(task)
    return True


@tool()
def get_all_todos():
    """Returns all the todos"""
    return todos

@tool()
def add_two_number(a: int, b: int):
    """This tool adds two int numbers"""
    return a + b

@tool()
def get_weather(city: str):
    """This tool returns the weather data about the given city"""

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."

    return "Something went wrong"

tools = [get_weather, add_two_number, add_todo, get_all_todos]

llm = init_chat_model(model_provider="openai", model="gpt-4.1-nano")
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    #messages ko add karega jab tak mera graph invoke nhi karega ,
    #jab graph invoke hoga tab pichla state jo hai remove ho jaayega 
    #lets say multiple nodes hai , graph unn sab ko chalyega , so annotated jo hai message mein information add karega 
    #jiise ki ek node ko dusre ka refernce mil sake , means tab tak llm ke pass memeory hai , jaise hi invoke hua naya state 
    #bnn jaayega 
    messages: Annotated[list, add_messages]
    
def chatBot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}

tool_node = ToolNode(tools=tools)
graph_builder = StateGraph(State)

#flow for this tool node is , start se chatBot chalega ,
# chatBot ke andar llm hai jisme tools bind hai ,
# to agar user ka query tool se related hua to tool chalega , 
# aur tool ke baad firse chatBot chalega taki user ko response mil sake
graph_builder.add_node("chatBot", chatBot)
graph_builder.add_node("tools", tool_node)

# path define karna hai , start se chatBot aur chatBot se end
graph_builder.add_edge(START, "chatBot")
graph_builder.add_edge("chatBot", END)

graph_builder.add_conditional_edges(
    "chatBot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatBot")

graph=graph_builder.compile()


def main():
    while True:
        user_query = input("> ")

        state = State(
            messages=[{"role": "user", "content": user_query}]
        )

        for event in graph.stream(state, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()


main()