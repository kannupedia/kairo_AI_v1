import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class GroqModel:
    def __init__(self):
        # Load env vars
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        env_path = os.path.join(base_dir, "backend", "APIs_and_configs", ".env")
        load_dotenv(env_path)

        # Load config
        config_path = os.path.join(base_dir, "backend", "APIs_and_configs", "config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {}

        model_name = config.get("groq_model_name", "llama-3.3-70b-versatile")
        temperature = config.get("temperature", 0.5)
        max_tokens = config.get("max_completion_tokens", 1024)
        
        # Verify API key
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key or api_key.strip() == "#ENTER YOUR GROQ API KEY HERE" or api_key.strip() == "":
            raise ValueError("GROQ_API_KEY is not set or invalid in .env file.")

        self.llm = ChatGroq(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key
        )
        self.history = []
        
        # Load prompt
        prompt_path = os.path.join(base_dir, "prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
        except Exception:
            system_prompt = "You are Kairo AI, a helpful assistant."
            
        self.history.append(SystemMessage(content=system_prompt))

    def generate_response(self, user_input):
        self.history.append(HumanMessage(content=user_input))
        try:
            response = self.llm.invoke(self.history)
            self.history.append(AIMessage(content=response.content))
            return response.content
        except Exception as e:
            return f"Error: Failed to connect to Groq LLM. Details: {str(e)}"
