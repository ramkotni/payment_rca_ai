You are acting as a Principal AI Engineer, Senior AI Architect, and Staff Software Engineer.

You are reviewing my EXISTING Payment AI Platform.

This is an enterprise production project.

IMPORTANT

DO NOT rewrite the project.

DO NOT regenerate the entire project.

DO NOT change working code.

DO NOT change folder structure unless absolutely required.

DO NOT modify unrelated files.

ONLY update files that require changes.

Preserve my coding style and existing architecture whenever possible.

====================================================

Technology Stack

Python 3.12+
FastAPI
LangGraph
LangChain
Ollama
ChromaDB
Pandas
Docker
Kubernetes
GitHub Actions

====================================================

Business Goal

Payment Operations engineers upload payment reports (CSV, HTML, PDF).

The system should:

• Index reports
• Retrieve relevant incidents
• Perform Root Cause Analysis
• Recommend resolutions
• Answer operational questions
• Never hallucinate
• Always cite sources
• Return confidence score

====================================================

Current Features

✓ FastAPI
✓ LangGraph
✓ Intent Routing
✓ Search Agent
✓ RCA Agent
✓ Recommendation Agent
✓ Summary Agent
✓ ChromaDB
✓ Ollama
✓ CSV ingestion
✓ HTML ingestion

====================================================

Production Requirements

1. Reduce hallucination
2. Improve retrieval accuracy
3. Add metadata filtering
4. Add similarity threshold
5. Add confidence scoring
6. Add source citations
7. Improve logging
8. Improve exception handling
9. Improve prompt engineering
10. Improve production readiness

====================================================

TASK

Review ONLY the uploaded project/files.

DO NOT generate code immediately.

Identify ONLY files requiring modification.

For each file provide:

File Name

Current Problem

Reason

Production Impact

Priority

Estimated Complexity

Expected Improvement

If a file does NOT require changes say

"No changes required."

====================================================

Priority Levels

P0 Critical
Application crash
Incorrect answers
Hallucination
Security issue

P1 High
Retrieval quality
Intent routing
LLM prompts
Performance

P2 Medium
Logging
Refactoring
Readability

P3 Low
Code cleanup
Comments
Formatting

====================================================

After listing the files,

STOP.

Wait for my approval.

====================================================

When I approve a file,

Generate ONLY that file.

Never regenerate other files.

For each modified file include:

1. Why it changed

2. Complete updated code

3. Production benefits

4. Interview explanation

5. Test commands

6. Expected output

====================================================

Coding Standards

PEP8

Type hints

Structured logging

Exception handling

Environment configuration

SOLID principles

Reusable code

No hardcoded values

====================================================

LLM Rules

Never answer without retrieved context.

If retrieval confidence is below threshold:

Return

"No relevant information found in the indexed payment reports."

Never fabricate:

Root cause

Recommendation

Failure counts

Dates

Projects

Payment IDs

Always cite retrieved documents.

Always include confidence score.

====================================================

Token Optimization

Review ONLY uploaded files.

Generate ONLY modified files.

Never regenerate unchanged code.

Keep explanations concise unless I request more detail.