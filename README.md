# Local AI Research Agent

A Streamlit interface for a LangChain agent that uses a local Ollama language model and DuckDuckGo Search to research questions that may require current web information.

## Features

- Streamlit interface for entering research questions
- Local inference through Ollama
- DuckDuckGo web-search tool
- Configurable Ollama model, endpoint, and temperature
- Optional terminal logging
- Markdown export of the final answer
- Error messages with expandable technical details

## Architecture

```text
User question
     |
     v
Streamlit UI
     |
     v
LangChain agent <------> DuckDuckGo Search
     |
     v
Ollama local model
     |
     v
Research answer
```

## Requirements

- Python 3.10–3.12 recommended
- [Ollama](https://ollama.com/) installed and running
- A model available in Ollama, such as `llama3.3`
- Internet access for DuckDuckGo searches

## Installation

### 1. Clone or download the project

```bash
git clone https://github.com/Sahusaksham333/langchain_duckduckgo_streamlit_project.git
cd langchain_duckduckgo_streamlit_project
```

If you downloaded the ZIP, extract it and open a terminal in the project directory.

### 2. Create a virtual environment

Using `venv`:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Alternatively, create a Conda environment:

```bash
conda create -n research-agent python=3.11 -y
conda activate research-agent
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start Ollama and download a model

Ensure the Ollama service is running, then execute:

```bash
ollama pull llama3.3
```

If you prefer another installed model, enter its name in the Streamlit sidebar. The model must already be available to the Ollama server.

By default, the app connects to:

```text
http://localhost:11434
```

You can change the endpoint in the sidebar. If Ollama runs inside another container or machine, `localhost` may not refer to that service; use a reachable host address instead.

### 5. Launch Streamlit

```bash
streamlit run app.py
```

Streamlit will print a local URL, typically `http://localhost:8501`.

## Usage

1. Enter a research question, such as **“What are the top technology jobs in India, and which skills are most frequently requested?”**
2. Select the Ollama model and adjust temperature in the sidebar.
3. Click **Run research**.
4. Review the response and optionally download it as a Markdown file.

## Troubleshooting

### Ollama connection error

- Confirm Ollama is installed and running.
- Check that the endpoint in the sidebar is reachable.
- Run `ollama list` to verify that the model is installed.

### Model not found

Download the model or enter the exact name shown by `ollama list`.

### Search errors

DuckDuckGo search is an external service and may occasionally throttle or change its behaviour. Retry later if a request fails.

### Slow responses or memory errors

Use a smaller Ollama model, reduce the prompt's scope, or run Ollama on a machine with sufficient available RAM/VRAM.

## Important limitations

- Search results can be incomplete, stale, or incorrect. Verify important claims against the original sources.
- The agent may not consistently provide complete source URLs in its prose.
- This project uses LangChain's legacy `initialize_agent` interface for compatibility with the supplied example. Consider migrating to a current LangChain/LangGraph agent pattern for a new production application.
- Do not treat the generated output as a substitute for independent verification.

## Project structure

```text
langchain-duckduckgo-streamlit/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## License

Choose a license before publishing or distributing this project. No license is implied by this repository template.
