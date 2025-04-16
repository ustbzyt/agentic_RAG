# Multi-Framework Agent Implementation Comparison

## Project Goal

This project implements a conversational agent with access to various tools using distinct Python frameworks. The primary goal is to compare and contrast the development experience, performance, observability features, and architectural patterns offered by each framework when building the same agent functionality.

## Functionality Implemented

The core functionality implemented across the frameworks is a **conversational agent** capable of:

*   Answering user questions.
*   Utilizing a set of tools to gather information:
    *   Retrieving information about specific guests (using a local dataset).
    *   Fetching current weather information.
    *   *(Note: HubStatsTool and Web Search are currently implemented only in smol-agents, but can be added to others)*
*   Interacting with the user via:
    *   A Gradio web interface (`smol-agents`).
    *   A command-line interface (`LangGraph`).
*   (Optional) Sending execution traces to Langfuse for observability.

## Frameworks

The following frameworks are being used or are planned for this comparison:

1.  **`smol-agents`**: (Implementation Complete in `agent_smolagents`) - smol-agents Documentation
2.  **`LangGraph`**: (Implementation Complete in `agent_langgraph`) - LangGraph Documentation
3.  **[TODO: LlamaIndex/Other]**: (Planned / In Progress - represented by `llama` argument) - [Link to Framework documentation]

## Current Status

*   The implementation using **`smol-agents`** is complete and functional (`agent_smolagents` directory, Gradio UI).
*   The implementation using **`LangGraph`** is complete and functional (`agent_langgraph` directory, CLI).
*   Implementations for the next framework (e.g., LlamaIndex) are planned.

## Project Structure

/Unit_3_Agentic_RAG             (Project Root)
|
|-- /agent_smolagents           (smol-agents implementation)
|   |-- app.py                  (Gradio UI logic - *called by main.py*)
|   |-- tools.py                (Custom tool definitions)
|   |-- retriever.py            (Guest dataset loading and retrieval tool)
|   |-- tracing.py              (Langfuse OpenTelemetry tracing setup)
|   |-- ...
|
|-- /agent_langgraph            (LangGraph implementation)
|   |-- app.py                  (CLI logic - *called by main.py*)
|   |-- agent_core.py           (LangGraph graph definition)
|   |-- agent_state.py          (Definition of the AgentState)
|   |-- nodes.py                (Graph node logic - assistant, tools)
|   |-- utils.py                (Tool definitions, LLM setup, agent_runnable)
|   |-- retriever.py            (Guest dataset loading and retrieval tool)
|   |-- prepare_dataset.py      (Helper for loading guest data)
|   |-- langfuse_client.py      (Langfuse handler setup)
|   |-- ...
|
|-- /agent_framework_c          (Placeholder for next framework)
|   |-- ...
|
|-- main.py                     (Top-level script to select and run agents)
|-- requirements.txt            (Python dependencies for the entire project)
|-- .env.example                (Example environment variables)
|-- README.md

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ustbzyt/agentic_RAG.git
    cd Unit_3_Agentic_RAG
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    *   Install all required packages from the root `requirements.txt` file:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure Environment Variables:**
    *   Copy the `.env.example` file to `.env`:
        ```bash
        # On Windows
        copy .env.example .env
        # On macOS/Linux
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your API keys:
        *   `GEMINI_API_KEY`: Your API key for Google Gemini (used by both smol-agents via LiteLLM and LangGraph via langchain-google-genai).
        *   `LANGFUSE_PUBLIC_KEY`: Your Langfuse Public Key (optional, for tracing).
        *   `LANGFUSE_SECRET_KEY`: Your Langfuse Secret Key (optional, for tracing).
        *   `OPENWEATHERMAP_API_KEY`: Your OpenWeatherMap API key.
        *   `HUGGINGFACEHUB_API_TOKEN`: Your Hugging Face API token (used by HubStatsTool in smol-agents).
        *   `OPENAI_API_KEY`: Your OpenAI API key (optional, if you choose to use OpenAI models).

## Usage

The `main.py` script is used to launch the desired agent implementation.

**Command:**

```bash
python main.py {smol,llama,graph}
Arguments:

smol: Runs the agent implemented using the smol-agents framework (launches Gradio UI).
llama: Placeholder for the next framework implementation (e.g., LlamaIndex).
graph: Runs the agent implemented using LangGraph (runs in the command line).
Examples:

To run the smol-agents version (Gradio UI):

bash
python main.py smol
Then open the provided local URL (e.g., http://127.0.0.1:7860) in your browser.

To run the LangGraph version (CLI):

bash
python main.py graph
Interact with the agent directly in your terminal.

Observability
Both the smol-agents and LangGraph implementations include optional integration with Langfuse for tracing agent execution. If you provide your Langfuse API keys in the .env file, detailed traces of the agent's thinking process, tool usage, and LLM calls will be sent to your Langfuse project.

For smol-agents, see agent_smolagents/tracing.py.
For LangGraph, see agent_langgraph/langfuse_client.py and how langfuse_handler is used.
plaintext

**Key Changes:**

*   Updated **Functionality Implemented** to mention both Gradio and CLI interfaces.
*   Updated **Frameworks** and **Current Status** to include LangGraph.
*   Updated **Project Structure** to show LangGraph files and note that `main.py` calls the respective `app.py` files.
*   Simplified **Setup** as `requirements.txt` is at the root.
*   Completely revamped the **Usage** section to explain the `main.py` arguments and provide clear examples for running `smol` and `graph`.
*   Updated **Observability** to mention LangGraph's Langfuse integration.

This looks much clearer and accurately reflects how to run your different agent implementations!