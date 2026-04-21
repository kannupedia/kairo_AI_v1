Kairo AI v1

Kairo AI v1 is a modular and developer-friendly AI system designed to integrate large language models within a clean, scalable architecture for building and managing AI-driven workflows efficiently.

Features

Modular Architecture: Clean and well-organized folder structure separating backend, models, and utilities
LLM Integration: Support for Groq-powered LLaMA 3.3 (70B Versatile) model
Configuration Management: Uses .env and config.json for flexible and secure configuration
Custom Tag Processing: Structured prompt parsing handled via tags.py
Centralized Logging: Integrated logging system using logger.py and logs/ directory
Prompt-driven Behavior Control: AI behavior can be dynamically controlled through prompt.txt
Scalable Backend Design: Architecture prepared for future API expansion and feature additions

Requirements

Python 3.10 or higher
Dependencies listed in requirements.txt

Installation

pip install -r requirements.txt

Prompt Setup

The core behavior of Kairo AI is defined through the prompt.txt file.

Use this link to get the prompt:
https://gist.github.com/kannupedia/abc2ca343a51179a104958f67c34a3e3

Steps

Open the link
Copy the full content
Paste it into prompt.txt

Running the Project

python main.py

Ensure that .env and config.json are properly configured before execution.

Notes

Logs are stored in the logs/ directory
Model-specific implementations are in backend/models/
The tag-based parsing system supports structured workflows
