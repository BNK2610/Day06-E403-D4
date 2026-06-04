try:
    from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

    print("Imported AgentExecutor and create_tool_calling_agent from langchain_classic.agents")
except ImportError as exc:
    print(f"Failed to import LangChain classic agent APIs: {exc}")

try:
    from langchain_openai import ChatOpenAI

    print("Imported ChatOpenAI from langchain_openai")
except ImportError as exc:
    print(f"Failed to import ChatOpenAI: {exc}")
