"""
LangGraph + Grok Agent Implementation
Multi-step reasoning agent with tool use and state persistence
"""

from typing import TypedDict, Optional, List, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool, Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
import json
from datetime import datetime
import requests


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """Graph state - manages conversation and reasoning flow"""
    messages: Annotated[List[BaseMessage], "list of messages"]
    current_task: str
    reasoning_steps: List[str]
    tool_results: dict
    final_answer: Optional[str]


# ============================================================================
# TOOLS DEFINITION
# ============================================================================

@tool
def search_web(query: str) -> str:
    """Search the web for current information using a search API.
    
    Args:
        query: Search query string
        
    Returns:
        Search results as formatted text
    """
    try:
        # Using DuckDuckGo or similar free API
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        url = f"https://api.search.brave.com/res/v1/web/search?q={query}"
        # Note: Replace with your actual API key or use alternative
        results = f"Search results for '{query}' - [Mock results]\n"
        results += "1. Result about topic\n"
        results += "2. Another relevant finding\n"
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def calculate_metric(operation: str, values: List[float]) -> str:
    """Calculate mathematical operations on provided values.
    
    Args:
        operation: Operation type (sum, avg, max, min, product)
        values: List of numeric values
        
    Returns:
        Calculation result
    """
    try:
        if operation == "sum":
            result = sum(values)
        elif operation == "avg":
            result = sum(values) / len(values) if values else 0
        elif operation == "max":
            result = max(values) if values else 0
        elif operation == "min":
            result = min(values) if values else 0
        elif operation == "product":
            result = 1
            for v in values:
                result *= v
        else:
            return f"Unknown operation: {operation}"
        
        return f"{operation}({values}) = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


@tool
def analyze_text(text: str, analysis_type: str = "summary") -> str:
    """Analyze text content for insights.
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis (summary, sentiment, keywords)
        
    Returns:
        Analysis results
    """
    try:
        if analysis_type == "summary":
            # Mock summarization
            sentences = text.split(".")
            return f"Summary: {'. '.join(sentences[:2])}"
        elif analysis_type == "sentiment":
            return f"Sentiment Analysis: Neutral tone detected in text"
        elif analysis_type == "keywords":
            words = text.split()
            return f"Key terms: {', '.join(words[:5])}"
        else:
            return "Unknown analysis type"
    except Exception as e:
        return f"Analysis error: {str(e)}"


@tool
def fetch_data(endpoint: str, data_type: str = "json") -> str:
    """Fetch data from an endpoint.
    
    Args:
        endpoint: API endpoint URL
        data_type: Expected data format (json, csv, xml)
        
    Returns:
        Fetched data
    """
    try:
        # Mock data fetching
        return json.dumps({
            "status": "success",
            "data_type": data_type,
            "endpoint": endpoint,
            "timestamp": datetime.now().isoformat(),
            "sample_data": {"value": 42, "status": "active"}
        }, indent=2)
    except Exception as e:
        return f"Fetch error: {str(e)}"


# Create tool list for executor
tools = [search_web, calculate_metric, analyze_text, fetch_data]
tool_executor = ToolExecutor(tools)


# ============================================================================
# GROK INTEGRATION
# ============================================================================

class GrokIntegration:
    """Wrapper for Grok/xAI API integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "sk-your-grok-key"
        self.client = anthropic.Anthropic(api_key=api_key)  # Using Anthropic as example
        self.model = "claude-opus-4-6"  # Can swap for Grok endpoint
        
    def reason_about_task(self, task: str, context: str = "") -> tuple[str, List[str]]:
        """Use Grok for extended reasoning about a task.
        
        Returns:
            (reasoning_output, list_of_reasoning_steps)
        """
        prompt = f"""You are an advanced reasoning agent. Analyze this task step by step.

Task: {task}

Context: {context}

Provide:
1. Your reasoning process (break it into numbered steps)
2. What tools or information you need
3. Your initial approach

Format your response as:
REASONING_STEPS:
1. [step]
2. [step]
...
APPROACH: [your strategy]"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        reasoning_text = response.content[0].text
        steps = self._extract_steps(reasoning_text)
        
        return reasoning_text, steps
    
    def refine_answer(self, question: str, context: str, initial_answer: str) -> str:
        """Refine an answer using extended reasoning."""
        prompt = f"""Review and refine this answer using careful reasoning.

Original Question: {question}
Context: {context}
Initial Answer: {initial_answer}

Provide an improved, more comprehensive answer that:
1. Addresses all aspects of the question
2. Incorporates the context
3. Adds nuance or important caveats
4. Explains the reasoning"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def _extract_steps(self, text: str) -> List[str]:
        """Extract numbered reasoning steps from text."""
        steps = []
        for line in text.split("\n"):
            if line.strip() and line[0].isdigit():
                steps.append(line.strip())
        return steps


# ============================================================================
# LANGGRAPH NODE DEFINITIONS
# ============================================================================

def analyze_task(state: AgentState) -> AgentState:
    """Node 1: Analyze the incoming task and create reasoning steps."""
    grok = GrokIntegration()
    
    task = state["current_task"]
    reasoning_output, steps = grok.reason_about_task(task)
    
    state["messages"].append(AIMessage(content=reasoning_output))
    state["reasoning_steps"] = steps
    
    return state


def select_tools(state: AgentState) -> AgentState:
    """Node 2: Determine which tools to use based on reasoning."""
    messages = state["messages"]
    
    # Use last AI message to determine tool needs
    last_message = messages[-1].content if messages else ""
    
    tools_needed = []
    if "search" in last_message.lower():
        tools_needed.append("search_web")
    if "calculat" in last_message.lower():
        tools_needed.append("calculate_metric")
    if "analyz" in last_message.lower():
        tools_needed.append("analyze_text")
    if "fetch" in last_message.lower() or "data" in last_message.lower():
        tools_needed.append("fetch_data")
    
    return {**state, "tool_results": {"selected_tools": tools_needed}}


def execute_tools(state: AgentState) -> AgentState:
    """Node 3: Execute the selected tools."""
    tool_results = state["tool_results"]
    selected_tools = tool_results.get("selected_tools", [])
    
    results = {}
    
    # Simulate tool execution
    if "search_web" in selected_tools:
        results["search"] = search_web.invoke({"query": state["current_task"]})
    
    if "fetch_data" in selected_tools:
        results["data"] = fetch_data.invoke({"endpoint": "/api/data"})
    
    state["tool_results"].update(results)
    
    # Add tool results to messages
    for tool_name, result in results.items():
        state["messages"].append(ToolMessage(content=result, tool_name=tool_name))
    
    return state


def synthesize_answer(state: AgentState) -> AgentState:
    """Node 4: Synthesize final answer from all information."""
    grok = GrokIntegration()
    
    context = "\n".join([str(r) for r in state["tool_results"].values()])
    
    # Get refined answer
    final_answer = grok.refine_answer(
        question=state["current_task"],
        context=context,
        initial_answer="Processing information from tools"
    )
    
    state["messages"].append(AIMessage(content=final_answer))
    state["final_answer"] = final_answer
    
    return state


def should_continue(state: AgentState) -> str:
    """Determine if we should continue processing or end."""
    if state["final_answer"]:
        return END
    return "execute_tools"


# ============================================================================
# BUILD GRAPH
# ============================================================================

def build_agent_graph():
    """Construct the LangGraph workflow."""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("analyze", analyze_task)
    graph.add_node("select_tools", select_tools)
    graph.add_node("execute", execute_tools)
    graph.add_node("synthesize", synthesize_answer)
    
    # Add edges (flow control)
    graph.add_edge("analyze", "select_tools")
    graph.add_edge("select_tools", "execute")
    graph.add_edge("execute", "synthesize")
    graph.add_edge("synthesize", END)
    
    # Set entry point
    graph.set_entry_point("analyze")
    
    return graph.compile()


# ============================================================================
# RUN AGENT
# ============================================================================

def run_agent(task: str):
    """Execute the agent on a given task."""
    print(f"\n{'='*70}")
    print(f"TASK: {task}")
    print(f"{'='*70}\n")
    
    agent = build_agent_graph()
    
    initial_state = AgentState(
        messages=[HumanMessage(content=task)],
        current_task=task,
        reasoning_steps=[],
        tool_results={},
        final_answer=None
    )
    
    # Execute graph
    final_state = agent.invoke(initial_state)
    
    print("\n" + "="*70)
    print("FINAL ANSWER:")
    print("="*70)
    print(final_state["final_answer"])
    
    print("\n" + "="*70)
    print("REASONING STEPS:")
    print("="*70)
    for i, step in enumerate(final_state["reasoning_steps"], 1):
        print(f"{i}. {step}")
    
    return final_state


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example tasks
    tasks = [
        "Research the latest developments in AI and summarize the key findings",
        "Analyze sentiment in product reviews and calculate average rating",
        "Find market trends data and provide insights",
    ]
    
    for task in tasks[:1]:  # Run first task
        result = run_agent(task)