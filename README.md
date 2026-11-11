# 🔎 Smart Search Agent

A conversational AI research assistant built with **Streamlit,
LangChain, and Groq**. It can search the web, retrieve encyclopedic
information from Wikipedia, and find academic research papers from
arXiv. The agent selects the appropriate search tool based on the user's
question and uses the returned results to generate an answer.

## ✨ Features

-   **Conversational interface:** Ask questions through a Streamlit chat
    interface.
-   **Web search:** Uses DuckDuckGo for general web results and recent
    information.
-   **Wikipedia search:** Retrieves factual and encyclopedic
    information.
-   **Academic research:** Searches arXiv for research papers.
-   **Tool-calling agent:** Uses LangChain tool calling with a
    Groq-hosted language model to decide when a search tool is needed.
-   **Multi-step search:** Can call tools across multiple iterations
    when a question needs more research.
-   **Live activity panel:** Displays the selected tool, search input,
    execution status, and search results.
-   **Chat controls:** Keeps conversation history during the session and
    provides a Clear Chat option.
-   **Configurable iterations:** Adjust the maximum number of agent
    iterations from the sidebar.

## 🧰 Tech Stack

  Category                          Technologies
  --------------------------------- --------------
  Frontend                          Streamlit
  LLM provider                      Groq
  LLM integration and agent tools   LangChain
  Web search                        DuckDuckGo
  Encyclopedic search               Wikipedia
  Research paper search             arXiv
  Language                          Python

## 📁 Project Structure

``` text
smart-search-agent/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Prerequisites

-   Python 3.10 or later
-   A Groq API key
-   Internet connection for the search tools

## 🚀 Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the repository URL and folder name with your own GitHub
repository details.

### 2. Create a virtual environment

**Windows (Command Prompt):**

``` cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the application

``` bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

``` text
http://localhost:8501
```

### 5. Add your Groq API key

1.  Open the application in your browser.
2.  Enter your Groq API key in the **Groq API Key** field in the
    sidebar.
3.  Select the available model.
4.  Ask a question in the chat box.

The API key is entered at runtime through Streamlit's password field.
**Do not hard-code your API key or commit it to GitHub.**

## 🔍 Available Search Tools

  Tool         Purpose
  ------------ ----------------------------------------------------
  DuckDuckGo   General web searches, recent information, and news
  Wikipedia    Factual and encyclopedic information
  arXiv        Academic papers and research topics

The agent can answer straightforward questions directly. When external
information is needed, it can select one or more tools, process their
results, and use those results to prepare its response.

## 🖥️ Using the Application

1.  Enter your Groq API key in the sidebar.
2.  Type a question in the chat input.
3.  Observe the activity panel to see which tool the agent selects.
4.  Expand the search-results section to inspect retrieved information.
5.  Continue the conversation with follow-up questions.
6.  Use **Clear Chat** to reset the conversation.

The **Max Agent Iterations** setting controls how many tool-calling
rounds the agent can perform for a question.

## 📦 Dependencies

Project dependencies are listed in `requirements.txt`:

-   `streamlit`
-   `langchain`
-   `langchain-groq`
-   `langchain-community`
-   `langchain-core`
-   `wikipedia`
-   `arxiv`
-   `duckduckgo-search`
-   `ddgs`

## 🔐 Security Notes

-   Keep your Groq API key private.
-   Do not upload API keys, passwords, or private configuration files to
    GitHub.
-   If you accidentally publish a key, revoke it and generate a new one.
-   Review dependency versions and update them when needed.

## ⚠️ Limitations

-   Search results depend on the availability and quality of the
    external search services.
-   The application requires a valid Groq API key to generate LLM
    responses.
-   Answers should be checked against the original sources, especially
    for important or time-sensitive research.
-   The model and available iteration range are currently configured in
    the application code.

## 📌 Future Improvements

-   Add source links and citations to generated answers.
-   Add support for more research and data sources.
-   Allow users to select from multiple language models.
-   Add persistent chat history.
-   Add export options for research results.

## 👨‍💻 Author

**YOUR NAME**

-   GitHub: [YOUR-GITHUB-PROFILE](https://github.com/YOUR-USERNAME)

------------------------------------------------------------------------

If you find this project useful, feel free to ⭐ the repository.
