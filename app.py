
import os
import streamlit as st
from langchain.agents import AgentType, Tool, initialize_agent
from langchain_community.llms import Ollama
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun

st.set_page_config(
    page_title="Local AI Research Agent",
    page_icon="🔎",
    layout="wide",
)

st.title("Local AI Research Agent")
st.caption("Web research powered by DuckDuckGo and local Ollama.")

with st.sidebar:
    st.header("Configuration")

    model_name = st.text_input(
        "Ollama model",
        value="llama3:latest",
    )

    ollama_base_url = st.text_input(
        "Ollama URL",
        value=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
    )

    verbose = st.checkbox(
        "Show agent logs in terminal",
        value=False,
    )

st.markdown(
    "Enter a question to search the web and generate a research summary."
)

prompt = st.text_area(
    "Research question",
    value=(
        "What are the top 10 trending technology jobs in India? "
        "Include key skills and source URLs."
    ),
    height=120,
)

col1, col2 = st.columns([1, 5])

with col1:
    run_search = st.button(
        "Run research",
        type="primary",
        use_container_width=True,
    )

with col2:
    clear_result = st.button("Clear previous result")

if clear_result:
    st.session_state.pop("last_response", None)
    st.rerun()

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if run_search:
    if not prompt.strip():
        st.warning("Please enter a research question.")
    elif not model_name.strip():
        st.warning("Please enter an Ollama model name.")
    else:
        try:
            with st.spinner("Researching your question..."):
                search = DuckDuckGoSearchRun()

                search_tool = Tool(
                    name="DuckDuckGo Search",
                    func=search.run,
                    description=(
                        "Search the web for recent facts, technology trends, "
                        "and external information. Include source URLs when "
                        "they are available in the results."
                    ),
                )

                llm = Ollama(
                    model=model_name.strip(),
                    base_url=ollama_base_url.strip().rstrip("/"),
                    temperature=temperature,
                )

                agent = initialize_agent(
                    tools=[search_tool],
                    llm=llm,
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=verbose,
                    handle_parsing_errors=True,
                    max_iterations=6,
                    early_stopping_method="generate",
                )

                result = agent.invoke(
                    {"input": prompt.strip()}
                )

                st.session_state.last_response = result.get(
                    "output",
                    "No answer was returned.",
                )

        except Exception as exc:
            st.error(
                "Research failed. Check Ollama, the model name, "
                "your internet connection, and dependencies."
            )

            with st.expander("Technical details"):
                st.code(f"{type(exc).__name__}: {exc}")

if st.session_state.last_response:
    st.subheader("Research results")
    st.markdown(st.session_state.last_response)

    st.download_button(
        "Download answer as Markdown",
        data=st.session_state.last_response,
        file_name="research_results.md",
        mime="text/markdown",
    )

with st.expander("Setup and troubleshooting"):
    st.markdown(
        """
        1. Install Python and Ollama.
        2. Run `ollama pull llama3:latest`.
        3. Install dependencies using `pip install -r requirements.txt`.
        4. Start the app using `python -m streamlit run app.py`.

        Docker is not required.
        """
    )

st.divider()
st.caption("Made by Saksham Sahu")
