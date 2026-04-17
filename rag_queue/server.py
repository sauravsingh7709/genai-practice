# flake8: noqa

from fastapi import FastAPI,Query
from .queue.connection import queue
from .queue.worker import process_query

app=FastAPI()

@app.get('/')
def root():
    return {"status":"server is up and running"}

@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # query ko queue mein daalo
    # user ko bolo you message or job recieved 

    # process_query call hoga with the parameter query
    job=queue.enqueue(process_query, query)   
    print(f"Job is done {job.id}")
    return {"status": "queued","job_id": job.id}