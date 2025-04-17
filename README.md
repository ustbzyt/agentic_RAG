# Multi-Framework Agent Implementation Comparison

## Project Goal

This project implements a conversational agent named Alfred with access to various tools using three distinct Python frameworks. The primary goal is to compare and contrast the development experience, performance, observability features, and architectural patterns offered by each framework when building the same agent functionality.

## Functionality Implemented

The core functionality implemented across the frameworks is a **conversational agent** named Alfred capable of:

* Answering user questions
* Utilizing a set of tools to gather information:
    * Retrieving information about specific guests (using a local dataset)
    * Fetching current weather information
    * Performing web searches (using DuckDuckGo)
    * Fetching Hugging Face model statistics
* Interacting with the user via:
    * A Gradio web interface (`smol-agents`)
    * A command-line interface (`LangGraph` and `LlamaIndex`)
* Optional execution traces to Langfuse for observability

## Frameworks

The following frameworks are implemented in this project:

1. **`smol-agents`**: (Implementation Complete in `agent_smolagents`)
   - Uses Gradio for web interface
   - Implements all core tools
   - Supports Langfuse tracing
   - Features:
     - Clean separation of concerns
     - Robust error handling
     - Comprehensive logging
     - Easy tool integration

2. **`LangGraph`**: (Implementation Complete in `agent_langgraph`)
   - Uses CLI interface
   - Implements all core tools
   - Supports Langfuse tracing
   - Features:
     - Graph-based execution flow
     - State management
     - Flexible message handling
     - Robust error recovery

3. **`LlamaIndex`**: (Implementation Complete in `agent_llamaindex`)
   - Uses CLI interface
   - Implements all core tools
   - Uses ReActAgent for tool usage
   - Features:
     - ReAct-based reasoning
     - Clean architecture
     - Comprehensive logging
     - Robust error handling

## Project Structure

```
/agentic_RAG (Project Root) 
├── /agent_smolagents (smol-agents implementation) 
│   ├── app.py (Gradio UI logic)
│   ├── tools.py (Custom tool definitions)
│   ├── retriever.py (Guest dataset loading and retrieval)
│   ├── tracing.py (Langfuse OpenTelemetry tracing)
│   └── prepare_dataset.py (Dataset preparation)
├── /agent_langgraph (LangGraph implementation) 
│   ├── app.py (CLI logic)
│   ├── agent_core.py (Graph definition)
│   ├── agent_state.py (State management)
│   ├── nodes.py (Graph node logic)
│   ├── utils.py (Tool definitions and setup)
│   ├── retriever.py (Guest dataset handling)
│   ├── prepare_dataset.py (Dataset preparation)
│   └── langfuse_client.py (Langfuse integration)
├── /agent_llamaindex (LlamaIndex implementation)
│   ├── app.py (CLI logic)
│   ├── utils.py (Tool definitions and setup)
│   ├── retriever.py (Guest dataset handling)
│   └── prepare_dataset.py (Dataset preparation)
├── main.py (Top-level script to select and run agents)
├── requirements.txt (Project dependencies)
└── README.md
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ustbzyt/agentic_RAG.git
   cd agentic_RAG
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and add your API keys:
   - `GEMINI_API_KEY`: Google Gemini API key
   - `LANGFUSE_PUBLIC_KEY`: Langfuse Public Key (optional)
   - `LANGFUSE_SECRET_KEY`: Langfuse Secret Key (optional)
   - `OPENWEATHERMAP_API_KEY`: OpenWeatherMap API key
   - `HUGGINGFACEHUB_API_TOKEN`: Hugging Face API token

## Usage

Run the desired agent implementation:

```bash
python main.py {smol,llama,graph}
```

Arguments:
- `smol`: Runs the smol-agents version (Gradio UI)
- `llama`: Runs the LlamaIndex version (CLI)
- `graph`: Runs the LangGraph version (CLI)

## Observability

Both smol-agents and LangGraph implementations include optional integration with Langfuse for tracing agent execution. If you provide your Langfuse API keys in the `.env` file, detailed traces of the agent's thinking process, tool usage, and LLM calls will be sent to your Langfuse project.

## Error Handling and Logging

All implementations feature:
- Comprehensive error handling
- Detailed logging
- Graceful error recovery
- User-friendly error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.
