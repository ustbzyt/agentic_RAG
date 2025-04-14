# Multi-Framework Agent Implementation Comparison

## Project Goal

This project implements a conversational agent with access to various tools using three distinct Python frameworks. The primary goal is to compare and contrast the development experience, performance, observability features, and architectural patterns offered by each framework when building the same agent functionality.

## Functionality Implemented

The core functionality implemented across all frameworks is a **conversational agent (chatbot)** capable of:

*   Answering user questions.
*   Utilizing a set of tools to gather information:
    *   Retrieving information about specific guests (using a local dataset via `agent_smolagents.retriever`).
    *   Fetching current weather information (`agent_smolagents.tools.WeatherInfoTool`).
    *   Getting statistics from the Hugging Face Hub (`agent_smolagents.tools.HubStatsTool`).
    *   Performing web searches (`DuckDuckGoSearchTool` from `smolagents`).
*   Interacting with the user via a Gradio web interface.
*   (Optional) Sending execution traces to Langfuse for observability (`agent_smolagents.tracing`).

## Frameworks

The following frameworks are being used or are planned for this comparison:

1.  **`smol-agents`**: (Implementation Complete in `agent_smolagents`) - smol-agents Documentation
2.  **[TODO: Framework B Name]**: (Planned / In Progress) - [Link to Framework B documentation or website if desired]
3.  **[TODO: Framework C Name]**: (Planned / In Progress) - [Link to Framework C documentation or website if desired]

## Current Status

*   The implementation using the **`smol-agents`** framework is complete and functional within the `agent_smolagents` directory.
*   Implementations for **[Framework B Name]** and **[Framework C Name]** are planned or currently under development.

## Project Structure

/Unit_3_Agentic_RAG             (Project Root)
|
|-- /agent_smolagents           (smol-agents implementation)
|   |-- app.py                  (Main application logic and Gradio UI)
|   |-- tools.py                (Custom tool definitions)
|   |-- retriever.py            (Guest dataset loading and retrieval tool)
|   |-- tracing.py              (Langfuse OpenTelemetry tracing setup)
|   |-- requirements.txt        (Python dependencies)
|   |-- ...
|
|-- /agent_framework_b          (Placeholder for Framework B)
|   |-- ...
|
|-- /agent_framework_c          (Placeholder for Framework C)
|   |-- ...
|
|-- main.py                     (Top-level script to run different agents)
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

3.  **Install dependencies for the `smol-agents` implementation:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Install dependencies for other framework implementations similarly when available.)*

4.  **Configure Environment Variables:**
    *   Copy the `.env.example` file to `.env`:
        ```bash
        # On Windows
        copy .env.example .env
        # On macOS/Linux
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your API keys:
        *   `GEMINI_API_KEY`: Your API key for Google Gemini.
        *   `LANGFUSE_PUBLIC_KEY`: Your Langfuse Public Key (optional, for tracing).
        *   `LANGFUSE_SECRET_KEY`: Your Langfuse Secret Key (optional, for tracing).
        *   `OPENWEATHERMAP_API_KEY`: Your OpenWeatherMap API key.
        *   `HUGGINGFACEHUB_API_TOKEN`: Your Hugging Face Secret Key (optional, for tracing).

## Usage

### Running the `smol-agents` Implementation

1.  Ensure your virtual environment is activated and you are in the project root directory (`Unit_3_Agentic_RAG`).
2.  Run the agent using the main script:
    ```bash
    python main.py smol
    ```
3.  The script will print logs to the console, including the status of Langfuse tracing and tool initializations.
4.  Once ready, it will output:
    ```
    Launching Gradio UI with Gemini model via LiteLLM...
    * Running on local URL:  http://127.0.0.1:7860
    ```
5.  Open your web browser and navigate to `http://127.0.0.1:7860` to interact with the agent.

## Observability

The `smol-agents` implementation includes optional integration with Langfuse for tracing agent execution. If you provide your Langfuse API keys in the `.env` file, detailed traces of the agent's planning and tool usage will be sent to your Langfuse project, which can be helpful for debugging and understanding the agent's behavior. The `agent_smolagents/tracing.py` module handles this setup.

---
