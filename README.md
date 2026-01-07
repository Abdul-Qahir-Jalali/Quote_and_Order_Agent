# Agentic Quote & Order System

## What is this project?
This is an **Agentic AI** application designed to act as an intelligent furniture sales representative. Unlike simple chatbots, this **Agent** can "think" about what users want, providing accurate quotes and handling complex order flows autonomously.

It is built using a **Modular Architecture**, which means the code is organized into distinct, independent parts (like Legos). This makes the AI easy to upgrade, fix, and scale without breaking the whole system.

## Key Features

*   **🧠 Agentic AI**: Powered by advanced Large Language Models (LLMs) to understand context, intent, and nuance in customer conversations.
*   **🧩 Modular Design**: The project is split into clear modules (`API`, `Services`, `Core`), ensuring clean code that is easy for developers to understand and extend.
*   **⚡ Instant Quote Generation**: The Agent actively calculates prices and generates quotes in real-time during the conversation.
*   **🛒 Automated Order Processing**: Seamlessly converts chat interactions into confirmed orders.

## How to Run It

1.  **Start the Agent**:
    ```bash
    python -m app.main
    ```

2.  **Interact**:
    Open your browser at `http://127.0.0.1:8000` to chat with the agent.

## Project Structure (Modular Approach)
*   **`app/core`**: The brain (AI prompts and configuration).
*   **`app/services`**: The logic (handles calculations and business rules).
*   **`app/api`**: The communication (talks to the web interface).
*   **`app/db`**: The memory (stores order history).

## Technologies
*   **Python**: Core language.
*   **FastAPI**: High-performance web framework.
*   **AI/LLM**: The intelligence behind the agent.
