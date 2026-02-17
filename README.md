# LangChain WikiBot

A simple knowledge retrieval and chat agent built with FastAPI, LangChain, and Google Generative AI. The service accepts questions from clients, performs searches on Wikipedia using a custom LangChain tool, and returns fact-checked JSON-formatted responses.

## Features

- **Tool-based fact checking**: Uses a `search` tool to fetch Wikipedia extracts and generate answers.
- **FastAPI server** serving two endpoints:
  - `/ask` (in `langbot.py`): receives questions and returns a JSON response from the LLM agent.
  - `/chat/` (in `server.py`): proxy for the generic `graph_app` email/chat functionality (used by the Streamlit client).
- **Streamlit client** (`client.py`) provides a simple web UI for interacting with the API.
- **.env support** for API keys (e.g., `CHROMA_GOOGLE_GENAI_API_KEY`).

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manju-droid/wikipedia-agent.git
   cd wikipedia-agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # use `venv\Scripts\activate` on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or manually: fastapi uvicorn python-dotenv requests langchain langchain-google-genai streamlit
   ```

4. **Configure environment variables**
   Create a `.env` file at the project root with:
   ```env
   CHROMA_GOOGLE_GENAI_API_KEY=your_api_key_here
   ```

5. **Run the API server**
   ```bash
   python langbot.py          # serves /ask endpoint
   # and/or
   uvicorn server:app --reload  # serves /chat/ endpoint
   ```

6. **Launch the client (optional)**
   ```bash
   streamlit run client.py
   ```

## Usage

- Send a `POST` request with JSON `{ "question": "Your query" }` to `http://localhost:8000/ask`
- The response will be a verified fact summary returned by the LLM.

Example:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Who is Elon Musk?"}'
```

## Notes

- The agent is designed to **always** use the Wikipedia `search` tool; responses are formatted in strict JSON.
- The Streamlit client points to `/chat/` and expects the `server.py` endpoint, which currently proxies to an `emailbot.graph_app`.
- The repository currently ignores `venv/`, `.env`, and `*.db` files via `.gitignore`.

## License

This project is provided "as-is" for educational/demo purposes.
