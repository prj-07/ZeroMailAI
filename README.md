# ZeroMailAI

Agentic AI Impl for no pendiing mails .

## The "Zero-Cost" Tech Stack
Brain (LLM): Groq Cloud (Free API). It is incredibly fast and offers Llama 3 models for free, which is perfect for high-speed agentic demos.
Orchestration: LangGraph (Open Source). This handles the "cycles" (e.g., fetching  drafting asking for your approval).
Email Engine: Gmail API (Free via Google Cloud Console). This is the industry standard for programmatic email access.
Memory: SQLite (Built into Python). It allows your agent to remember which emails it has already "seen" so it doesn't double-process them.

## The Core Logic (Nodes)
An agent is just a collection of functions (Nodes) connected by logic (Edges).

Node 1: The Collector – Fetches unread emails from your multiple IDs.

Node 2: The Judge – Decides if an email is "Noise" (ignore) or "Signal" (requires action).

Node 3: The Drafter – Prepares a response based on the context.

Node 4: The Human Review – This is the most important part! The agent stops and waits for you to say "Yes, send it."