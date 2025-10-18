import importlib.metadata
packages = [
    "langgraph",
    "langchain_community",
    "langchain_core",
    "tavily-python",
    "wikipedia",
    "langchain-tavily",
    "ipykernel",
    "langchain_google_genai",
    "langchain_groq",
    "python-dotenv",
    "langchain_huggingface",
    "sentence-transformers",
    "chromadb",
    "langchain-openai"
    ]
for pkg in packages:
    try:
        version = importlib.metadata.version(pkg)
        print(f"{pkg}=={version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{pkg} (not installed)")