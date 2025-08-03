from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated 
import json
import datetime


app = FastAPI() 
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def About():
    about_description ="""
            ## About the Project
            
            This project focuses on analyzing real-world network traffic to uncover patterns, evaluate performance, and detect anomalies using big data techniques. The data                originates from the [CSE-CIC-IDS2018 dataset](https://www.unb.ca/cic/datasets/ids-2018.html), a collaborative cybersecurity initiative by the Communications                   Security Establishment (CSE) and the Canadian Institute for Cybersecurity (CIC). It was accessed via [Kaggle](https://www.kaggle.com/datasets/karenp/original-                 network-traffic-tuesday-20-02-2018-pcap) and is also available on the [AWS Open Data Registry](https://registry.opendata.aws/cse-cic-ids2018).
            
            ### Project Goal
            
            The primary goal is to analyze network performance through structured data extraction and visualization. The analysis is divided into three main parts:
            
            #### Part One – General Information Extraction
            This stage involves extracting basic metrics such as:
            * Total number of captured packets
            * Frame and IP packet volumes
            * Capture duration and intervals
            * Average, minimum, and maximum packet sizes
            * Number of unique IP addresses
            * Top communicators (top talkers)
            * Detection of checksum errors and malformed packets
            
            #### Part Two – Time-Based Analysis
            A time-series analysis using one-minute intervals to evaluate:
            * Average frames per minute
            * Frame count over time
            * Cumulative traffic volume growth
            
            #### Part Three – Field Value Distribution
            This includes:
            * Distribution of IP flags
            * Protocol usage visualization (e.g., bar plots)
            
            ### Technical Approach
            
            Due to the large data volume (~45GB) and the inefficiency of directly processing `.cap` files in Spark, the workflow includes:
            * Manually unzipping the dataset
            * Extracting key packet-level fields using Scapy's `Ether` module
            * Converting data to Parquet format using the custom `CapToParquet.py` module
            * Running analysis with Apache Spark (PySpark) for scalable performance
            
            Users can directly work with the provided Parquet files or generate them from `.cap` files using the provided module in this repository.
           
            """
    return {"description": about_description}

@app.get('/partone')
async def dashboard():
    try:
        
        with open('data_partone.json', 'r') as file:
            data = json.load(file)
            return data 
    
    except Exception as e:
        raise HTTPException(status =500,detail = f"there has been an error in reading the JSON file: {e}")  
    
@app.get('/parttwo')
async def dashboard():
    try:
        
        with open('data_partwo.json', 'r') as file:
            data = json.load(file)
            return data 
    
    except Exception as e:
        raise HTTPException(status =500,detail = f"there has been an error in reading the JSON file: {e}")  

@app.get('/parthree')
async def dashboard():
    try:
        
        with open('data_parthree.json', 'r') as file:
            data = json.load(file)
            return data 
    
    except Exception as e:
        raise HTTPException(status =500,detail = f"there has been an error in reading the JSON file: {e}") 