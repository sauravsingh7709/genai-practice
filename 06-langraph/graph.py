from langgraph import graph
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client=OpenAI()

class State(TypedDict):
    query: str
    llm_result: str|None

def chat_bot(state: State):

    # State mein se query lao 
    query=state['query']
    # LLM se result lao
    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"user","content":query}
            ]
        )
    # State mein result update karo

    result=response.choices[0].message.content
    state['llm_result']=result

    return state

# 1st step: graph banate hain
graph_builder=StateGraph(State)
#2nd step: graph mein nodes add karte hain , nodes means simple functions jo kaam karwana hain
graph_builder.add_node("chat_bot", chat_bot)
#3rd step: graph mein edges add karte hain , edges means ki kaunse node
#  ke baad kaunse node ko run karna hai

#START se chat_bot ko run karna hai aur chat_bot ke baad END ko run karna hai
graph_builder.add_edge(START,"chat_bot")
graph_builder.add_edge("chat_bot",END)

#4th step : graph ko compile karte hain
graph=graph_builder.compile()

def main():
    user=input("> ")

    # Invoke the graph
    _state={
        "query":user,
        "llm_result":None
    }

    graph_result=graph.invoke(_state)
    print(graph_result)

main()