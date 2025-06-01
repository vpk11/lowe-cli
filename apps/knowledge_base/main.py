from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
def read_root():
    with open("knowledge_base.json", "r") as f:
        knowledge_base_data = json.load(f)
    return knowledge_base_data
    
