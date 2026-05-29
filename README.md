# 🚀 Hybrid Autonomous Agent OS

A hybrid multi-agent AI operating system that intelligently routes tasks between **local models** and **cloud LLMs**, maintains persistent memory, performs planning and verification, and provides an interactive web interface.

Built with **LangGraph**, **Transformers**, **ChromaDB**, **LiteLLM**, and **Gradio**.

---

## 🌟 Features

### 🧠 Intelligent Task Routing

Automatically routes requests to the most suitable AI engine:

* **Local Model** for fast, low-cost tasks
* **Cloud LLM** for complex reasoning and research

This hybrid approach balances speed, cost, and quality.

---

### 📋 Autonomous Planning Agent

Complex tasks are decomposed into structured execution plans before processing.

**Example**

Input:

```text
Build an AI healthcare startup roadmap
```

Planner Output:

```text
1. Market Research
2. Product Strategy
3. Technical Architecture
4. MVP Development
5. Go-To-Market Plan
```

---

### 🔧 Tool Recommendation Agent

Suggests external tools when required.

Current capabilities:

* Python execution suggestions
* Web search suggestions

Future integrations:

* Browsers
* APIs
* Databases
* Code interpreters
* Autonomous tool execution

---

### ☁️ Local + Cloud AI Execution

#### Local Agent

Model:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

Best suited for:

* Grammar correction
* Summarization
* Translation
* Small coding tasks
* Fast responses

#### Cloud Agent

Powered through:

```text
OpenRouter
GPT-OSS-120B
```

Best suited for:

* Research
* Strategic planning
* Startup analysis
* System design
* Long-form reasoning

---

### ✅ Response Verification

Every response is automatically evaluated before being returned.

Workflow:

```text
Generate Response
        ↓
Verify Output
        ↓
PASS → Return Result
FAIL → Repair Agent
```

---

### 🔄 Self-Repair Mechanism

If verification fails:

1. Analyze the response
2. Identify weaknesses
3. Generate an improved version
4. Return repaired output

This creates a lightweight autonomous quality-control loop.

---

### 🧠 Persistent Memory

Uses ChromaDB for long-term memory storage.

Capabilities:

* Context retrieval
* Previous interaction recall
* Memory compression
* Improved continuity across sessions

Stored format:

```text
USER: Question
AI: Response
```

---

### 🌐 Gradio User Interface

Interactive dashboard displaying:

* Execution route
* Planner output
* Tool recommendations
* Final AI response

---

## 🏗️ System Architecture

```text
                 User Input
                      │
                      ▼
              ┌────────────┐
              │  Router    │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Planner    │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Tool Agent │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Execution  │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │ Verifier   │
              └─────┬──────┘
                    │
          PASS      │      FAIL
            │       │        │
            ▼       │        ▼
           END      │   Repair Agent
                    │        │
                    └────────┘
```

---

## 🛠️ Tech Stack

| Component       | Technology                  |
| --------------- | --------------------------- |
| Workflow Engine | LangGraph                   |
| Local Model     | Qwen2.5-0.5B-Instruct       |
| Cloud Model     | GPT-OSS-120B via OpenRouter |
| Memory Layer    | ChromaDB                    |
| User Interface  | Gradio                      |
| LLM Routing     | LiteLLM                     |
| Inference       | Hugging Face Transformers   |
| Backend         | Python                      |
| Acceleration    | PyTorch + Accelerate        |

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/hybrid-autonomous-agent-os.git

cd hybrid-autonomous-agent-os
```

### Install Dependencies

```bash
pip install langgraph langchain langchain-community langchain-core

pip install transformers accelerate bitsandbytes sentence-transformers

pip install chromadb

pip install gradio

pip install litellm
```

---

## 🔑 Configuration

Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="YOUR_API_KEY"
```

Or inside Python:

```python
import os

os.environ["OPENROUTER_API_KEY"] = "YOUR_API_KEY"
```

---

## ▶️ Running the Project

Launch the notebook or application:

```bash
python app.py
```

or

```bash
jupyter notebook
```

The Gradio interface will launch automatically.

---

## 📖 Example Usage

### Fast Local Task

```text
Summarize AI in 3 bullet points
```

```text
Translate this paragraph into French
```

```text
Fix grammar mistakes in this email
```

---

### Advanced Cloud Task

```text
Research AI startup opportunities in healthcare
```

```text
Design a scalable multi-agent architecture
```

```text
Create a SaaS growth strategy roadmap
```

---

## 📂 Project Structure

```text
Hybrid-Autonomous-Agent-OS/
│
├── app.py
├── Hybrid_Autonomous_Agent_OS.ipynb
├── README.md
│
├── memory/
│   └── chroma_storage
│
├── agents/
│   ├── router.py
│   ├── planner.py
│   ├── verifier.py
│   └── repair.py
│
└── ui/
    └── gradio_app.py
```

> The current notebook implementation can later be refactored into modular Python packages as shown above.

---

## 🚀 Future Roadmap

Planned improvements:

* Real web search integration
* Retrieval-Augmented Generation (RAG)
* Autonomous tool execution
* Multi-model routing
* Cost-aware inference
* Streaming responses
* Agent collaboration
* Docker deployment
* Kubernetes support
* Observability and tracing
* Evaluation benchmarks

---

## ⚠️ Current Limitations

* Rule-based routing logic
* Basic verification workflow
* Lightweight memory retrieval
* Tool suggestions only (no execution)
* Single local model
* No streaming output

---

## 🤝 Contributing

Contributions are welcome.

Ideas for contributions:

* Smarter routing strategies
* Better verification mechanisms
* Enhanced memory systems
* New tool integrations
* Additional local model support
* UI improvements

Steps:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a pull request

---

## 📄 License

MIT License

You are free to use, modify, distribute, and build upon this project.

---

## 🙏 Acknowledgements

Built using:

* LangGraph
* Hugging Face Transformers
* ChromaDB
* LiteLLM
* Gradio
* OpenRouter

Special thanks to the open-source AI community for advancing autonomous agent systems.

---

⭐ If you find this project useful, consider starring the repository and sharing it with others.
