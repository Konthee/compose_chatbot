import json
import logging
from glob import glob
from typing import Any, List, Optional
from pydantic import BaseModel
import uuid

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fastapi import FastAPI, File, status, UploadFile,Form
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_qdrant import FastEmbedSparse, RetrievalMode
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from tog_chatbot import LLMClient


app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
)

# Output
class ResponseChat(BaseModel):
    response :  str
    session_id:  str
    reference: Optional[Any] = None


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")


@app.post("/chat",response_model=ResponseChat)
async def chat(
    user_message: str = Form(..., description="Enter user message"),
    session_id: str = Form("", description="Enter session_id"),
):
    session_id = session_id or str(uuid.uuid4())

    # This is where you can add llm with api

    return ResponseChat(response =user_message,session_id=session_id)


@app.post("/chat_rag",response_model=ResponseChat)
async def chat_rag(
    user_message: str = Form(..., description="Enter user message"),
    session_id: str = Form("", description="Enter session_id"),
):
    session_id = session_id or str(uuid.uuid4())

    # This is where you can add your custom pipelines like RAG.

    return ResponseChat(response =user_message,session_id=session_id)



@app.post("/chat_sql",response_model=ResponseChat)
async def chat_sql(
    user_message: str = Form(..., description="Enter user message"),
    session_id: str = Form("", description="Enter session_id"),
):
    session_id = session_id or str(uuid.uuid4())

    # This is where you can add your custom pipelines like sql.

    return ResponseChat(response =user_message,session_id=session_id)



@app.post("/chat_pipeline",response_model=ResponseChat)
async def chat_pipeline(
    user_message: str = Form(..., description="Enter user message"),
    session_id: str = Form("", description="Enter session_id"),
):
    session_id = session_id or str(uuid.uuid4())

    # This is where you can add your custom pipelines 

    return ResponseChat(response =user_message,session_id=session_id)