# 🚀 LangGraph Grok Agent

A production-ready **Agentic AI** project built with **LangGraph**, **Groq**, and **Python** that demonstrates graph-based AI workflows, multi-step reasoning, tool calling, state persistence, and reactive agents.

This repository contains both a **basic LangGraph agent** and an **advanced reactive agent**, making it a great starting point for learning modern AI agent development.

---

## ✨ Features

* 🤖 LangGraph-powered AI Agents
* ⚡ Groq LLM Integration
* 🔄 Graph-based Workflow Execution
* 🛠️ Tool Calling
* 🧠 Multi-step Reasoning
* 💬 Stateful Conversations
* 💾 Checkpoint Support
* 📜 Execution Logging
* 🔧 Environment Variable Configuration
* 🚀 FastAPI Deployment Example
* 📦 Modular Project Structure

---

# 📂 Project Structure

```text
langgraph-grok-agent/
├── langgraph_grok_agent.py          # Basic LangGraph agent implementation
├── langgraph_reactive_agent.py      # Advanced reactive AI agent
├── setup_and_config.py              # Configuration & utility functions
├── requirements.txt                 # Project dependencies
├── .env                             # API keys & environment variables
├── README.md                        # Project documentation
├── checkpoints/                     # Saved LangGraph checkpoints
├── logs/                            # Runtime logs
└── examples/
    ├── example_basic.py             # Basic usage example
    ├── example_advanced.py          # Advanced workflows
    └── example_api_server.py        # FastAPI deployment example
```

---

# ⚙️ Tech Stack

* Python 3.11+
* LangGraph
* LangChain
* Groq API
* Pydantic
* python-dotenv
* FastAPI
* Uvicorn

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Ronit049/LangGraph_Grok_Agent.git

cd langgraph-grok-agent
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

GEMINI_API_KEY=your_gemini_api_key
```

---

# ▶️ Running the Project

## Basic LangGraph Agent

```bash
python langgraph_grok_agent.py
```

---

## Reactive Agent

```bash
python langgraph_reactive_agent.py
```

---

## FastAPI Server

```bash
python examples/example_api_server.py
```

or

```bash
uvicorn examples.example_api_server:app --reload
```

---

# 📖 Examples

## Basic Example

```bash
python examples/example_basic.py
```

Demonstrates:

* Building a LangGraph workflow
* Executing an AI agent
* Managing graph state

---

## Advanced Example

```bash
python examples/example_advanced.py
```

Demonstrates:

* Multi-step reasoning
* Tool execution
* Dynamic routing
* Stateful conversations

---

## API Deployment

```bash
python examples/example_api_server.py
```

Demonstrates:

* FastAPI integration
* REST API endpoint
* JSON responses
* Production deployment

---

# 🧠 Agent Workflow

```text
User Input
     │
     ▼
Task Analysis
     │
     ▼
Reasoning
     │
     ▼
Tool Selection
     │
     ▼
Tool Execution
     │
     ▼
State Update
     │
     ▼
Response Generation
     │
     ▼
Final Answer
```

---

# 📦 Main Components

## `langgraph_grok_agent.py`

* Basic LangGraph workflow
* Tool execution
* Graph state management
* AI response generation

---

## `langgraph_reactive_agent.py`

* Advanced reactive agent
* Conditional routing
* Dynamic tool selection
* Multi-step reasoning
* Context-aware responses

---

## `setup_and_config.py`

* Environment configuration
* API initialization
* Logging setup
* Utility functions

---

# 📁 Checkpoints

The `checkpoints/` directory stores saved LangGraph execution states, allowing interrupted workflows to resume later.

---

# 📝 Logs

Execution logs are written to the `logs/` directory for debugging, monitoring, and tracing agent behavior.

---

# 🎯 Learning Objectives

This project demonstrates:

* LangGraph Fundamentals
* Agentic AI
* Graph-based AI Workflows
* Tool Calling
* State Persistence
* Multi-step Reasoning
* Prompt Engineering
* API Integration
* FastAPI Deployment

---

# 🚀 Future Improvements

* Memory Integration
* RAG (Retrieval-Augmented Generation)
* Multi-Agent Collaboration
* Streaming Responses
* Human-in-the-Loop Workflows
* Database Persistence
* Docker Support
* CI/CD Pipeline
* Cloud Deployment (Railway, Render, AWS)

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Ronit Raj**

Computer Science Engineering Student | Python Developer | Agentic AI Enthusiast

### Skills

* Python
* LangGraph
* LangChain
* Groq
* Gemini
* FastAPI
* AI Agents
* Machine Learning
* Generative AI

---

⭐ If you found this project useful, please **Star** the repository and consider contributing!
