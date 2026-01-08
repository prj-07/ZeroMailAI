import os
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_google_community import GmailToolkit

# 1. SETUP
os.environ["GROQ_API_KEY"] = ""
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# The toolkit will automatically look for 'token.json' in your folder
toolkit = GmailToolkit()
tools = toolkit.get_tools()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    emails_to_review: List[dict]
    action_required: bool

# 2. SIMPLIFIED NODES
def fetch_emails_node(state: AgentState):
    search_tool = next(t for t in tools if t.name == "search_gmail")
    
    # Let's target ONLY the Primary inbox to match your browser
    query = "is:unread category:primary" 
    results = search_tool.invoke({"query": query, "max_results": 25})
    
    print(f"\n--- 🔎 AI FOUND {len(results)} PRIMARY UNREAD EMAILS ---")
    for idx, email in enumerate(results):
        # We print the subject so you can recognize the email
        subject = email.get('subject', 'No Subject')
        print(f"[{idx+1}] {subject[:60]}...") 
    print("-------------------------------------------\n")
    
    return {"emails_to_review": results}

def classifier_node(state: AgentState):
    """AI decides if the first email needs attention."""
    if not state["emails_to_review"]:
        return {"action_required": False}
    
    email = state["emails_to_review"][0]
    prompt = f"Is this email important? {email['snippet']}. Reply YES or NO."
    res = llm.invoke(prompt)
    return {"action_required": "YES" in res.content.upper()}

# 3. GRAPH
workflow = StateGraph(AgentState)
workflow.add_node("fetcher", fetch_emails_node)
workflow.add_node("classifier", classifier_node)

workflow.add_edge(START, "fetcher")
workflow.add_edge("fetcher", "classifier")
workflow.add_edge("classifier", END)

app = workflow.compile()

if __name__ == "__main__":
    app.invoke({"messages": []})