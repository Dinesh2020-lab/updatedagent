
import streamlit as st

from langchain_groq import ChatGroq

from langchain_community.utilities import (
    WikipediaAPIWrapper,
    ArxivAPIWrapper
)

from langchain_community.tools import (
    WikipediaQueryRun,
    ArxivQueryRun,
    DuckDuckGoSearchRun
)

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)


# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Smart Search Agent",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Smart Search Agent")

st.caption(
    "Powered by Groq · LangChain · Wikipedia · Arxiv · DuckDuckGo"
)


# ──────────────────────────────────────────────
# SIDEBAR SETTINGS
# ──────────────────────────────────────────────

st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_..."
)

model_name = st.sidebar.selectbox(
    "Model",
    ["openai/gpt-oss-120b"],
    index=0
)

max_iterations = st.sidebar.slider(
    "Max Agent Iterations",
    3,
    15,
    7
)

st.sidebar.markdown("---")

if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi 👋 Ask me anything!"
        }
    ]

    st.rerun()


# ──────────────────────────────────────────────
# SEARCH TOOLS
# ──────────────────────────────────────────────

wiki_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=2,
        doc_content_chars_max=800
    )
)

wiki_tool.description = (
    "Search Wikipedia for factual and encyclopedic "
    "information about people, places, history, "
    "science and concepts."
)

arxiv_tool = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper(
        top_k_results=2,
        doc_content_chars_max=600
    )
)

arxiv_tool.description = (
    "Search Arxiv for academic research papers. "
    "Use a short topic or paper title."
)

search_tool = DuckDuckGoSearchRun(
    name="DuckDuckGo"
)

search_tool.description = (
    "Search the internet for current events, news, "
    "recent information and general web results."
)

tools = [
    search_tool,
    arxiv_tool,
    wiki_tool
]

tool_map = {
    tool.name: tool for tool in tools
}


# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi 👋 Ask me anything! I can search the web, "
                "Wikipedia, Arxiv and help with research."
            )
        }
    ]


# DISPLAY CHAT HISTORY

for msg in st.session_state.messages:

    st.chat_message(msg["role"]).write(
        msg["content"]
    )


# ──────────────────────────────────────────────
# GROQ TOOL-CALLING AGENT
# ──────────────────────────────────────────────

def run_agent(user_input, activity):

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=0
    )

    # BIND TOOLS TO GROQ

    llm_with_tools = llm.bind_tools(tools)

    system_prompt = SystemMessage(
        content="""
        You are Smart Search Agent, a helpful research assistant.

        Available tools:

        1. DuckDuckGo:
           Use for recent information, news and web searches.

        2. Wikipedia:
           Use for encyclopedic and factual information.

        3. Arxiv:
           Use for academic research papers.

        Instructions:
        - Select the appropriate tool when external information
          is required.
        - Use multiple tools when necessary.
        - Never invent search results.
        - If information is unavailable, say so.
        - Give clear and accurate answers.
        - Answer simple general questions directly when possible.
        """
    )

    # BUILD CONVERSATION HISTORY

    conversation = [system_prompt]

    # Exclude the current user message because it is
    # appended separately below.

    for msg in st.session_state.messages[:-1]:

        if msg["role"] == "user":

            conversation.append(
                HumanMessage(content=msg["content"])
            )

        elif msg["role"] == "assistant":

            conversation.append(
                AIMessage(content=msg["content"])
            )

    conversation.append(
        HumanMessage(content=user_input)
    )

    # TOOL-CALLING LOOP

    for iteration in range(max_iterations):

        response = llm_with_tools.invoke(
            conversation
        )

        conversation.append(response)

        # CHECK TOOL SELECTION

        if not response.tool_calls:

            activity.write("✅ Final answer generated.")

            return response.content

        # EXECUTE SELECTED TOOLS

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            # DISPLAY SELECTED TOOL

            activity.markdown(
                f"### 🔧 Selected Tool: {tool_name}"
            )

            activity.markdown(
                f"**Search Input:** `{tool_args}`"
            )

            # EXECUTE TOOL

            if tool_name not in tool_map:

                tool_result = "Requested tool is unavailable."

                activity.error(
                    "❌ Tool not found."
                )

            else:

                try:

                    with st.spinner(
                        f"Executing {tool_name}..."
                    ):

                        tool_result = tool_map[
                            tool_name
                        ].invoke(tool_args)

                    activity.success(
                        f"✅ {tool_name} executed successfully."
                    )

                    with activity.expander(
                        "View search results"
                    ):

                        st.write(str(tool_result))

                except Exception as error:

                    tool_result = (
                        f"Tool execution failed: {str(error)}"
                    )

                    activity.error(
                        f"❌ {tool_name} failed: {error}"
                    )

            # SEND TOOL RESULT BACK TO GROQ

            conversation.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_id
                )
            )

    # FINAL RESPONSE AFTER ITERATION LIMIT

    activity.warning(
        "Maximum tool iterations reached. Generating final response."
    )

    conversation.append(
        SystemMessage(
            content=(
                "Do not request more tools. "
                "Provide the best possible answer using "
                "the information already collected."
            )
        )
    )

    final_response = llm.invoke(
        conversation
    )

    activity.write("✅ Final answer generated.")

    return final_response.content


# ──────────────────────────────────────────────
# CHAT INPUT
# ──────────────────────────────────────────────

if user_input := st.chat_input("Ask anything..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.chat_message("user").write(user_input)

    if not api_key:

        st.warning(
            "⚠️ Please enter your Groq API key in the sidebar."
        )

        st.stop()

    with st.chat_message("assistant"):

        # LIVE AGENT ACTIVITY PANEL

        with st.status(
            "🔎 Agent is working...",
            expanded=True
        ) as activity:

            try:

                response = run_agent(
                    user_input,
                    activity
                )

                activity.update(
                    label="✅ Search completed",
                    state="complete",
                    expanded=False
                )

            except Exception as error:

                response = (
                    f"⚠️ Agent error: {str(error)}"
                )

                activity.update(
                    label="❌ Agent failed",
                    state="error",
                    expanded=True
                )

        st.write(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
