from fastapi import FastAPI, HTTPException
from emailbot import graph_app
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

app = FastAPI()

class Chatrequest(BaseModel):
    message: str
    thread_id : str="1"

@app.post("/chat/")

def chat_endpoint(request: Chatrequest):
    """
    Input: User message + User ID
    Output: The AI's response (or tool result)
    """
    try:
     config = {"configurable" : {"thread_id": request.thread_id}}
     response = graph_app.invoke({"messages": [HumanMessage(content=request.message)]}, config=config)
     final_response = response["messages"][-1].content

     return{
        "response": final_response,
        "thread_id": request.thread_id
     }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))