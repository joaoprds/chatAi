
from langgraph.graph import StateGraph, START, END

from app.ai.state import AgentState
from app.ai.client import client
from app.ai.tool_definitions import tools
from app.ai.agent import execute_tool
from app.core.config import settings


MAX_TOOL_ROUNDS = 5


INSTRUCTIONS = """
You are an enterprise operations assistant.

You can answer questions about products, inventory,
customers and orders.

Rules:
- Use available tools when business data is required.
- Never invent inventory quantities or order information.
- Only use information returned by the tools.
- If a tool reports that information was not found,
  communicate that clearly.
- You are a read-only assistant.
- Never claim that you modified business data.
- Answer in the same language as the user.
"""


# NODE 1: LLM

def agent_node(state: AgentState):

    response = client.responses.create(
        model=settings.openai_model,
        instructions=INSTRUCTIONS,
        input=state["input_items"],
        tools=tools,
    )

    function_calls = [
        item for item in response.output
        if item.type == "function_call"
    ]

    if not function_calls:
        return {
            "answer": response.output_text,
            "pending_calls": [],
        }

    response_items = [
        item.model_dump(exclude_none=True)
        for item in response.output
    ]

    pending_calls = [
        item.model_dump(exclude_none=True)
        for item in function_calls
    ]

    return {
        "input_items": state["input_items"] + response_items,
        "pending_calls": pending_calls,
    }


# NODE 2: TOOL EXECUTION

def tools_node(state: AgentState):

    results = []

    for tool_call in state["pending_calls"]:

        result = execute_tool(
            db=None,  # Will be replaced with injected DB session
            company_id=state["company_id"],
            tool_name=tool_call["name"],
            arguments=tool_call["arguments"],
        )

        results.append({
            "type": "function_call_output",
            "call_id": tool_call["call_id"],
            "output": str(result),
        })

    return {
        "input_items": state["input_items"] + results,
        "pending_calls": [],
        "tool_rounds": state["tool_rounds"] + 1,
    }


# ROUTING

def route_after_agent(state: AgentState):

    if not state["pending_calls"]:
        return END

    if state["tool_rounds"] >= MAX_TOOL_ROUNDS:
        raise RuntimeError(
            "Maximum tool execution rounds exceeded."
        )

    return "tools"


# GRAPH DEFINITION

builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", tools_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

agent_graph = builder.compile()
