import os
from dotenv import load_dotenv
from research_analyst.exception.custom_exception import ResearchAnalystException
from research_analyst.logger import GLOBAL_LOGGER as log
from research_analyst.utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
import asyncio

class APIMANAGER:

    def __init__(self):
        self.api_key = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
            "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "LANGSMITH_API_KEY": os.getenv("LANGSMITH_API_KEY"),
            "LANGSMITH_TRACING_V2": os.getenv("LANGSMITH_TRACING_V2"),
            "LANGSMITH_PROJECT": os.getenv("LANGSMITH_PROJECT")
        }

        for key,vals in self.api_key.items():
            if vals is None:
                log.error(f"{key} is not set in environment variables.")
                raise ResearchAnalystException(f"{key} is not set in environment variables.")
            log.info("All required API keys are set.")

    def get_key(self, key: str):
        return self.api_key.get(key)
    
class ModelLoader:
    def __init__(self):
        load_dotenv()
        self.api_manager = APIMANAGER()
        self.config = load_config()

    def load_embedding_model(self):
        try:
            model_name = self.config['embedding']['model_name']
            log.info("Loading Google Generative AI Embedding Model")
            api_key = self.api_manager.get_key("GOOGLE_API_KEY")
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())

            embedding_model = GoogleGenerativeAIEmbeddings(model=model_name, api_key=api_key)
            log.info(f"Successfully loaded embedding model: {model_name}")
            return embedding_model
        
        except Exception as e:
            log.error(f"Error loading embedding model: {e}")
            raise ResearchAnalystException(f"Error loading embedding model: {e}")

    def load_llm_model(self):

        try:
            llm_block = self.config.get('llm')
            provider_key=os.getenv("LLM_PROVIDER","google")
            
            if provider_key not in llm_block:
                raise ResearchAnalystException(f"LLM provider '{provider_key}' not found in configuration.")
            
            llm_config = llm_block[provider_key]
            provider=llm_config.get('provider')
            model_name=llm_config.get('model_name')
            temperature=llm_config.get('temperature',0.2)
            log.info(f"Loading LLM Model from provider: {provider_key}")

            if provider_key == "groq":
                api_key = self.api_manager.get_key("GROQ_API_KEY")
                llm_model = ChatGroq(api_key=api_key, model=model_name, temperature=temperature)

            
            elif provider_key == "google":
                api_key = self.api_manager.get_key("GOOGLE_API_KEY")
                llm_model = ChatGoogleGenerativeAI(api_key=api_key, model=model_name, temperature=temperature)

            elif provider_key == "openai":
                api_key = self.api_manager.get_key("OPENAI_API_KEY")
                llm_model = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=temperature)

            else:
                raise ResearchAnalystException(f"Unsupported LLM provider: {provider_key}")
            
            log.info(f"Successfully loaded LLM model: {model_name} from provider: {provider_key}")
            return llm_model
        
        except Exception as e:
            log.error(f"Error loading LLM model: {e}")
            raise ResearchAnalystException(f"Error loading LLM model: {e}")

if __name__ == "__main__":
    loader = ModelLoader()
    embedding_model = loader.load_embedding_model()
    print(embedding_model.embed_query("Hello, world!"))

    llm = loader.load_llm_model()
    print(llm.invoke("WHAT is the capital of INDIA?"))
