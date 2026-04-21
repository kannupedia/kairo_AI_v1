import importlib.util
import os

file_path = os.path.join(os.path.dirname(__file__), "groq_llama-3.3-70B-versatile.py")
spec = importlib.util.spec_from_file_location("groq_model", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

GroqModel = module.GroqModel
