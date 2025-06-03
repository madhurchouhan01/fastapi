# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from digi_ad.chat_bot import DigiState, DigiFlow
# from typing import Dict

# app = FastAPI(title="Question Answering API", version="1.0.0")

# class QuestionRequest(BaseModel):
#     name: str
#     email: str
#     question: str

# class AnswerResponse(BaseModel):
#     answer: str

# @app.post("/ask", response_model=AnswerResponse)
# async def ask_question(payload: QuestionRequest):
#     """Endpoint to handle user questions"""
#     if not payload.question.strip():
#         raise HTTPException(status_code=400, detail="Question cannot be empty.")

#     # Initialize state with user data
#     st_state = DigiState(
#         creds={
#             "name": payload.name,
#             "email": payload.email,
#         },
#         user_query=payload.question
#     )
    
#     # Execute chatbot flow
#     flow = DigiFlow(st_state=st_state)
#     flow.kickoff()
    
#     return AnswerResponse(answer=flow.state.final_result["result"])

# @app.get("/ping")
# def ping():
#     return {"message": "pong"}

from digi_ad.chat_bot import DigiState, DigiFlow
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

app = FastAPI(title="Question Answering API", version="1.0.0")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
class QuestionRequest(BaseModel):
    name: str
    email: str
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):   

    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    st_state = DigiState(
        creds={
            "name": payload.name,
            "email": payload.email,
        },
        user_query=payload.question
    )
    
    # Execute chatbot flow
    flow = DigiFlow(st_state=st_state)
    flow.kickoff()
    
    return AnswerResponse(answer=flow.state.final_result["result"])

@app.get("/ping")
def ping():
    return {"message": "pong"}
