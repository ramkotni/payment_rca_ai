1. Business Problem
Existing Process

ERCOT Operations team receives payment failure reports daily.

Reports are generated as:

CSV files
HTML reports
Email notifications

When a payment fails, support teams manually:

Open reports
Search historical incidents
Find root causes
Identify resolutions

This process is slow and error-prone.

Business Goal

Build an AI-powered assistant that can answer:

Why did GINR123 fail?

What are the top payment failures in the last 3 months?

Show all duplicate payment issues.

using natural language.

2. High Level Architecture
User
 |
 v

FastAPI REST API
 |
 v

LangGraph Workflow
 |
 +----------------+
 |                |
Search Agent      |
 |                |
 v                |
ChromaDB          |
 |                |
 v                |
Payment Reports   |
                 |
RCA Agent --------+
 |
 v
Recommendation Agent
 |
 v
Summary Agent
 |
 v
Final Response
3. Project Structure
src/

api/
   main.py

agents/
   search_agent.py
   rca_agent.py
   recommendation_agent.py
   summary_agent.py

rag/
   ingest.py
   retriever.py
   embeddings.py

graph.py

data/

chroma_db/
4. Step 1 – Data Ingestion

File:

rag/ingest.py

Purpose:

Read all payment reports.

Example:

data/

payment_failures_2025-06.csv

payment_failures_2025-07.csv

payment_failures_2025-08.csv

Code:

df = pd.read_csv(file)

Example row:

project_id = GINR123

failure_type = FIS_FEE_UNPAID

severity = Critical

resolution = Customer contacted

Convert into document:

Document(
    page_content=text
)

Result:

Project ID: GINR123

Failure Type: FIS_FEE_UNPAID

Severity: Critical

Resolution: Customer contacted
5. Step 2 – Embedding Generation

File:

rag/embeddings.py

Code:

OllamaEmbeddings(
    model="nomic-embed-text"
)

Purpose:

Convert text into vectors.

Example:

"FIS Fee Missing"

becomes:

[0.234, 0.567, 0.891....]
6. Step 3 – Store in ChromaDB

Code:

Chroma.from_documents(...)

Creates:

chroma_db/

Now all payment failures become searchable.

7. Step 4 – Retriever

File:

rag/retriever.py

Code:

db = Chroma(
    persist_directory="./chroma_db"
)

Creates:

retriever = db.as_retriever()

Purpose:

Search similar incidents.

Example:

Question:

Why did GINR123 fail?

Retriever returns:

Project ID: GINR123

Failure:
FIS_FEE_UNPAID

Severity:
Critical

Resolution:
Customer contacted
8. Step 5 – LangGraph

File:

graph.py

This is the orchestration layer.

State:

class GraphState(TypedDict):

    question: str

    context: str

    root_cause: str

    recommendation: str

    answer: str

LangGraph passes state from node to node.

9. Search Agent

File:

search_agent.py

Input:

state["question"]

Example:

Why did GINR123 fail?

Code:

docs = retriever.invoke(
    state["question"]
)

Output:

state["context"]

Example:

Project ID: GINR123

Failure:
FIS_FEE_UNPAID
10. RCA Agent

File:

rca_agent.py

Purpose:

Perform Root Cause Analysis.

Prompt:

prompt = f"""
Analyze the issue.

Context:
{state['context']}
"""

LLM:

ChatOllama(
   model="gemma3:1b"
)

Output:

state["root_cause"]

Example:

FIS Fee was not received.
11. Recommendation Agent

File:

recommendation_agent.py

Input:

state["root_cause"]

Prompt:

Recommend corrective actions.

Output:

state["recommendation"]

Example:

Notify customer and re-initiate payment.
12. Summary Agent

File:

summary_agent.py

Input:

root_cause

recommendation

Output:

state["answer"]

Example:

GINR123 failed because the FIS fee was not received.
Customer should be contacted and payment re-initiated.
13. Graph Execution Flow
graph.invoke(
    {
        "question":
        "Why did GINR123 fail?"
    }
)

Execution:

START

↓

Search Agent

↓

RCA Agent

↓

Recommendation Agent

↓

Summary Agent

↓

END
14. FastAPI Layer

File:

api/main.py

API:

POST /ask

Request:

{
   "question":
   "Why did GINR123 fail?"
}
15. Runtime Flow

User sends request

↓

FastAPI receives request

↓

LangGraph invoked

↓

Search Agent

↓

Retriever searches ChromaDB

↓

RCA Agent analyzes

↓

Recommendation Agent suggests fix

↓

Summary Agent generates response

↓

FastAPI returns answer

16. Example Interview Explanation (2 Minutes)

The business problem was that payment failure investigations required manual analysis of CSV and HTML reports. Operations teams spent significant time searching historical incidents and identifying resolutions.

To solve this, I built an AI-powered Payment Failure Intelligence Platform using LangGraph, LangChain, Ollama, ChromaDB, and FastAPI.

Historical payment reports are ingested and converted into embeddings using the nomic-embed-text model. These embeddings are stored in ChromaDB for semantic search.

When a user asks a question, FastAPI invokes a LangGraph workflow. The Search Agent retrieves relevant incidents from ChromaDB, the RCA Agent performs root cause analysis, the Recommendation Agent suggests corrective actions, and the Summary Agent generates the final response.

This architecture reduced manual investigation effort, enabled conversational access to operational knowledge, and improved payment failure resolution time.

======
Understand the actual code execution path.

Project Execution Flow

When the user clicks Execute in Swagger UI:

POST /ask

the request flows through these major function calls.

Step 1: FastAPI Endpoint

Example:

@app.post("/ask")
def ask(req: AskRequest):

    result = graph.invoke({
        "question": req.question
    })

    return result
What happens?

User sends:

{
  "question": "Why are payment failures increasing?"
}

Execution enters:

graph.invoke()

This is the entry point of LangGraph.

Step 2: LangGraph Workflow

Usually:

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_context)
workflow.add_node("rca", rca_agent)
workflow.add_node("recommend", recommendation_agent)
workflow.add_node("summary", summary_agent)

workflow.set_entry_point("retrieve")

workflow.add_edge("retrieve", "rca")
workflow.add_edge("rca", "recommend")
workflow.add_edge("recommend", "summary")

graph = workflow.compile()
What compile() does
graph = workflow.compile()

Creates an executable graph.

Think of it like:

retrieve_context()
      ↓
rca_agent()
      ↓
recommendation_agent()
      ↓
summary_agent()
Step 3: graph.invoke()

Called from API:

result = graph.invoke({
    "question": req.question
})

Initial State:

{
   "question": "Why are payment failures increasing?"
}

LangGraph passes this state to the first node.

Step 4: retrieve_context()

Example:

def retrieve_context(state):

    docs = retriever.invoke(
        state["question"]
    )

    state["context"] = "\n".join(
        [doc.page_content for doc in docs]
    )

    return state
Important call
retriever.invoke()

Internally:

User Question
      ↓
Embedding Model
      ↓
Vector Search
      ↓
Top K Documents
Embedding Generation

Example:

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

Question:

Why are payment failures increasing?

Converted to:

[0.23, 0.56, 0.11, ...]

vector representation.

Chroma Search
docs = db.similarity_search(
    question,
    k=3
)

Internally:

Question Vector
       ↓
Chroma Vector DB
       ↓
Cosine Similarity Search
       ↓
Top 3 Documents

Returned:

[
   doc1,
   doc2,
   doc3
]
State Update

Before:

{
   "question":"..."
}

After:

{
   "question":"...",
   "context":"Gateway timeout log..."
}
Step 5: RCA Agent

Function:

def rca_agent(state):

Receives:

{
   "question":"...",
   "context":"..."
}
Prompt Creation
prompt = f"""
Context:
{state['context']}

Question:
{state['question']}
"""
LLM Call
response = llm.invoke(prompt)

Most important line.

Internally:

Prompt
   ↓
LangChain
   ↓
ChatOllama
   ↓
Ollama API
   ↓
llama3.2
   ↓
Response
ChatOllama
llm = ChatOllama(
    model="llama3.2"
)

LangChain sends:

POST localhost:11434/api/chat

to Ollama.

Model Reasoning

Llama receives:

Context:
Gateway timeout ...

Question:
Why are payment failures increasing?

Produces:

{
  "issue":"Gateway Timeout",
  "severity":"HIGH"
}
Store Result
state["root_cause"] = result
Step 6: Recommendation Agent

LangGraph automatically passes updated state.

recommendation_agent(state)

Receives:

{
   "question":"...",
   "context":"...",
   "root_cause": {...}
}
Another LLM Call
response = llm.invoke(prompt)

Prompt:

Based on root cause:

{state['root_cause']}

Returns:

{
  "recommendations":[]
}

Stored:

state["recommendation"]
Step 7: Summary Agent

Receives:

{
   "root_cause": {...},
   "recommendation": {...}
}
Final LLM Call
response = llm.invoke(prompt)

Combines everything.

Returns:

{
   "incident_summary":"...",
   "impact":"...",
   "priority":"HIGH"
}

Stored:

state["answer"]
Step 8: LangGraph Returns

Last node returns:

return state

LangGraph returns:

result = graph.invoke(...)

Result:

{
   "question":"...",
   "context":"...",
   "root_cause": {...},
   "recommendation": {...},
   "answer": {...}
}
Step 9: FastAPI Response
return result

FastAPI automatically converts Python dict to JSON:

{
   "answer": {
      "incident_summary":"...",
      "priority":"HIGH"
   }
}
Most Important Functions to Understand
FastAPI
@app.post()

Creates REST endpoint.

LangGraph
workflow.add_node()

Registers agent.

workflow.add_edge()

Connects agents.

workflow.compile()

Builds executable graph.

graph.invoke()

Runs workflow.

LangChain
llm.invoke(prompt)

Calls LLM.

Ollama
ChatOllama(
    model="llama3.2"
)

Connects LangChain to local Ollama server.

RAG
retriever.invoke(question)

Retrieves context.

Chroma
similarity_search()

Performs vector search.

For interviews, if you can confidently explain these 6 calls:

graph.invoke()

retriever.invoke()

similarity_search()

llm.invoke()

workflow.compile()

return state

you'll understand about 80% of the code execution path in your Payment AI Platform.