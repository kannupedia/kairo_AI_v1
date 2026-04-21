import os
import json
import importlib.util
from logger import logger

from backend.utils.tags import process_tags

# Dynamically import model because the folder has hyphens
model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", "models", "groq_llama-3.3-70B-versatile"))
model_init = os.path.join(model_dir, "__init__.py")

spec = importlib.util.spec_from_file_location("groq_llama_model", model_init)
model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_module)

GroqModel = model_module.GroqModel

def main():
    logger.info("Initializing Kairo AI v1...")
    
    # Load config to check if tags are enabled
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", "APIs_and_configs", "config.json"))
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        config = {}

    username = config.get("username", "User")
    use_tags = config.get("use_tags", True)
    
    logger.info("Loading model...")
    try:
        model = GroqModel()
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        print("Error: Could not initialize AI model. Check your API key and network connection.")
        return

    print("=========================================")
    print(f"       Kairo AI v1 - Welcome {username}!      ")
    print("=========================================")
    print("Type 'exit' or 'quit' to end the chat.")
    print("")

    while True:
        try:
            user_input = input(f"{username}: ")
            if user_input.lower() in ("exit", "quit", "q"):
                print("Kairo: Goodbye!")
                logger.info("User exited the chat.")
                break
                
            if not user_input.strip():
                continue

            logger.info(f"User Input: {user_input}")
            
            # Send to model
            response_text = model.generate_response(user_input)
            logger.info(f"Raw Model Output: {response_text}")
            
            # Process tags if enabled
            if use_tags:
                response_text = process_tags(response_text)
                logger.info(f"Processed Output: {response_text}")
                
            print(f"Kairo: {response_text}")
            
        except KeyboardInterrupt:
            print("\nKairo: Goodbye!")
            logger.info("Chat forcefully interrupted by user.")
            break
        except Exception as e:
            logger.error(f"Error during chat handling: {e}")
            print(f"Kairo: I encountered an error: {e}")

if __name__ == "__main__":
    main()
