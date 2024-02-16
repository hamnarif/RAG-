<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Conversational Question-Answering API with FastAPI</title>
</head>
<body>
  <h1>Conversational RAG API with FastAPI</h1>

  <p>This repository contains code for setting up a conversational question-answering API using FastAPI, GPT-4, and Supabase.</p>

  <h2>Overview</h2>

  <p>The conversational question-answering system is designed to interact with users. Users can input questions or prompts, and the system responds with relevant answers based on the conversation history and context. The system utilizes GPT-4all embeddings, mistral for language understanding and Supabase for storing and retrieving context embeddings.</p>

  <h2>Features</h2>

  <ul>
    <li>FastAPI web application for handling user input and generating AI responses.</li>
    <li>Cross-Origin Resource Sharing (CORS) middleware for allowing cross-origin requests.</li>
    <li>Support for processing user input, invoking the conversational QA model, and updating chat history.</li>
    <li>Health check endpoint for monitoring the status of the application.</li>
  </ul>

  <h2>Installation</h2>

  <ol>
    <li>Clone the repository:</li>
    <code>
      <pre>
git clone &lt;repository-url&gt;
cd RAG-
      </pre>
    </code>
    <li>Install dependencies:</li>
    <code>
      <pre>
pip install -r requirements.txt
      </pre>
    </code>
    <li>Set up environment variables:</li>
    <p>Create a <code>.env</code> file in the root directory and add the following variables:</p>
    <code>
      <pre>
SUPABASE_URL=&lt;your-supabase-url&gt;
SUPABASE_SERVICE_KEY=&lt;your-supabase-service-key&gt;
      </pre>
    </code>
    <p>Replace <code>&lt;your-supabase-url&gt;</code> and <code>&lt;your-supabase-service-key&gt;</code> with your Supabase URL and service key, respectively.</p>
  </ol>

  <h2>Usage</h2>

  <ol>
    <li>Run the FastAPI application:</li>
    <code>
      <pre>
uvicorn driver:app --reload
      </pre>
    </code>
    <li>Access the API at <code>http://localhost:8000</code>.</li>
    <li>Send POST requests to <code>/process_user_input/</code> endpoint with user input in the request body to get AI responses.</li>
    <li>Perform health check by sending a GET request to <code>/healthcheck</code> endpoint.</li>
  </ol>

  <h2>API Endpoints</h2>

  <ul>
    <li><code>POST /process_user_input/</code>: Endpoint to process user input and generate AI response.</li>
    <li><code>GET /healthcheck</code>: Endpoint for health check.</li>
  </ul>

  <h2>Contributing</h2>

  <p>Contributions are welcome! If you have any ideas for improvements or find any issues, please open an issue or submit a pull request.</p>

  <h2>Acknowledgements</h2>

  <ul>
    <li>This project utilizes FastAPI, GPT-4all, Supabase, and Mistral.</li>
  </ul>

</body>
</html>
