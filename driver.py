from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from model import conversational_qa_chain
from langchain_core.messages import HumanMessage

# Initialize FastAPI app
app = FastAPI()

# CORS Setup
origins = [
    "http://localhost",
    "http://localhost:3000", 
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model for user input
class UserInputRequest(BaseModel):
    user_input: str

# Initialize chat history
chat_history = []

@app.post("/process_user_input/")
async def process_user_input(request: UserInputRequest):
    """
    Endpoint to process user input and generate AI response.
    """
    global chat_history  # Accessing global chat history
    user_input = request.user_input  # Extract user input from request

    # Invoke conversational QA model with user input and chat history
    ai_msg = conversational_qa_chain.invoke({
        "question": user_input,
        "chat_history": chat_history,
    })

    # Update chat history with user input and AI response
    chat_history.extend([HumanMessage(content=user_input), ai_msg])
    
    # Convert AI message context to JSON-serializable format
    result_dict = jsonable_encoder(ai_msg.context)

    # Return AI response as JSON
    return JSONResponse(content={"answer": result_dict})  

@app.get("/healthcheck")
async def root():
    """
    Endpoint for health check.
    """
    return {"message": "Status: OK"}
