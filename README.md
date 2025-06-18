# FST Marrakech Chatbot

## Prerequisites

- **Node.js** (v18+ recommended) and **npm** (for the frontend)
- **Python** (v3.9+ recommended) and **pip** (for the backend)
- (Optional) **virtualenv** for Python environments

---

## Environment Variables

Before setting up the backend, you need to create a `.env` file in the `backend` directory with the following variables:

```env
# OpenAI API Key (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Vector Database (Required)
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=your_collection_name
```

**Important:**

- Replace all placeholder values with your actual credentials
- All environment variables are required - no default values are provided
- The `.env` file should never be committed to version control
- Make sure `.env` is listed in your `.gitignore` file

---

## Backend Setup (FastAPI)

1. **Navigate to the backend directory:**

   ```sh
   cd backend
   ```

2. **Install dependencies:**

   - Create and activate a virtual environment (recommended):
     ```sh
     python -m venv venv
     # On Unix/macOS:
     source venv/bin/activate
     # On Windows:
     venv\Scripts\activate
     ```
   - Install required packages:
     ```sh
     pip install fastapi uvicorn python-dotenv langchain langchain-openai langchain-qdrant qdrant-client
     ```

3. **Set up environment variables:**

   - Create a `.env` file in the `backend` directory and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Run the backend server:**
   ```sh
   uvicorn main:app --reload --port 8001
   ```

---

## Frontend Setup (Next.js/React)

1. **Navigate to the frontend directory:**

   ```sh
   cd frontend
   ```

2. **Install dependencies:**

   ```sh
   npm install
   ```

3. **Run the development server:**

   ```sh
   npm run dev
   ```

4. **Access the frontend:**
   - Open your browser and go to `http://localhost:3000`

---

## Connecting Frontend and Backend

- The frontend should send POST requests to `http://localhost:8001/chat` with a JSON body:
  ```json
  {
    "question": "Your question here",
    "session_id": "unique_session_id"
  }
  ```
- The backend will respond with:
  ```json
  {
    "answer": "Chatbot's response"
  }
  ```

---

## Health Check

- To verify the backend is running, visit: `http://localhost:8001/health`

---
