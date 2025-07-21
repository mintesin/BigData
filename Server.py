from fastapi import FastAPI,Query
from pydantic import BaseModel,Field
from typing import Annotated 
import datetime
from DataPreprocessor import ReadandCombine

app = FastAPI() 

@app.get('/')
async def visualize():
    return {"name": "visualization baord"}
