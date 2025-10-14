# AI Coding Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

An advanced AI-powered assistant designed to provide expert-level code reviews, optimizations, and conversational debugging to help developers write better code, faster.

---

##  Features

* **Intelligent, Multi-Persona Analysis:** The AI acts as a specific expert (e.g., Algorithm Judge, Performance Engineer, Code Stylist) based on the code's language and the user's selected goal.
* **Intent-Driven Goals:** Users can specify their objective, whether it's finding bugs, optimizing performance, improving style, generating unit tests, or simply explaining the code.
* **Multi-Language Support:** Provides expert analysis for **Python, Java, JavaScript, C++, C, and SQL**.
* **Conversational Chat:** A built-in, history-aware chat allows for interactive follow-up questions about the code, turning the tool into a true AI debugging partner.
* **Professional UI:** A clean, modern, IDE-like interface with a two-column layout and a polished design, built with Streamlit.
* **Robust Backend:** Powered by a reliable and synchronous FastAPI server for handling AI processing.

## Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Language:** Python
* **AI Model:** Google AI Platform (Generative Language API)

## Quick Start

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.10 or higher
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/[YOUR_REPOSITORY_NAME].git
    cd code-review-assistant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    * Create a new file named `.env` in the main project folder.
    * Add your Google AI API key to this file:
    ```
    GOOGLE_API_KEY="AIzaSy...your_secret_api_key..."
    ```

## Running the Application

This project requires two terminals to run simultaneously.

1.  **Terminal 1: Start the Backend Server**
    * Make sure your virtual environment is activated.
    ```bash
    uvicorn src.main:app
    ```
    * The API will be running at `http://127.0.0.1:8000`.

2.  **Terminal 2: Start the Frontend App**
    * Open a new terminal and activate the virtual environment.
    ```bash
    streamlit run dashboard.py
    ```
    * The application will open in your browser at `http://localhost:8501`.

## Architecture

The application uses a simple and robust client-server architecture:
