# 🤖 Distributed Multi-Agent Enterprise System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A distributed multi-agent system where specialized AI agents collaborate to solve complex enterprise tasks through hierarchical planning, consensus mechanisms, and human-in-the-loop oversight.

## 🚀 Key Features

### 👥 Agent Specialization
- **Research Agent**: Gathers information from multiple sources
- **Code Agent**: Generates and reviews code
- **Validation Agent**: Checks outputs for correctness
- **Security Agent**: Reviews for security vulnerabilities

### 🎯 Hierarchical Task Planning
- **Master Agent**: Decomposes complex tasks into subtasks
- **Worker Agents**: Execute subtasks in parallel
- **Result Aggregation**: Combines outputs into coherent results

### 🗳️ Consensus Mechanism
- **Voting System**: Multiple agents vote on critical decisions
- **Confidence Scoring**: Each agent provides confidence levels
- **Dispute Resolution**: Escalation paths for disagreements

### 👤 Human-in-the-Loop
- **Approval Gates**: Human approval for high-stakes decisions
- **Context Preservation**: Full context provided for human review
- **Feedback Loop**: Human feedback improves agent performance

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Master Orchestrator                          │
│                    (Task Decomposition)                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌──────▼────────┐  ┌──────▼────────┐
│  Research      │  │   Code        │  │  Validation   │
│  Agent         │  │   Agent       │  │  Agent        │
├────────────────┤  ├────────────────┤  ├────────────────┤
│ • Web search   │  │ • Generate    │  │ • Fact check  │
│ • API calls    │  │ • Review      │  │ • Test cases  │
│ • Data analysis│  │ • Refactor    │  │ • Assertions  │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Consensus & Aggregation                       │
│                   (Voting + Result Merge)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
     ┌────────▼────────┐      ┌─────────▼─────────┐
     │  Auto-Approve   │      │  Human Review     │
     │  (Low risk)     │      │  (High risk)      │
     └─────────────────┘      └───────────────────┘
```

## 📚 Usage

### Simple Task Execution

```python
from multi_agent import AgentOrchestrator

orchestrator = AgentOrchestrator()

result = await orchestrator.execute_task(
    task="Create a Python function to calculate customer LTV",
    context={"business_type": "ecommerce", "data_schema": {...}}
)

print(result.final_output)
print(result.agent_contributions)
print(result.confidence_score)
```

### Complex Multi-Agent Workflow

```python
workflow = {
    "task": "Build an API integration",
    "subtasks": [
        {"agent": "research", "task": "Research API documentation"},
        {"agent": "code", "task": "Generate integration code"},
        {"agent": "validation", "task": "Review and test code"},
        {"agent": "security", "task": "Security audit", "requires_approval": True}
    ]
}

result = await orchestrator.execute_workflow(workflow)
```

## 🛠️ Tech Stack

- **Python 3.11+** - Core language
- **LangGraph** - Agent orchestration
- **Temporal** - Durable workflow execution
- **Anthropic Claude** - LLM backend

## 👤 Author

**Pham Thach Son (Kent) Nguyen**
- Solutions Architect | AI & Systems Integration
- LinkedIn: [linkedin.com/in/kentnguyen93](https://linkedin.com/in/kentnguyen93)

## 📄 License

MIT License
