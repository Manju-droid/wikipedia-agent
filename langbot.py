import os
from dotenv import load_dotenv
import requests
from langchain.agents import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI    
from langchain.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()
api_key=os.getenv("CHROMA_GOOGLE_GENAI_API_KEY")

app = FastAPI()

wikiurl="https://en.wikipedia.org/w/api.php"
@tool
def search(topic:str)->str:
        """
        Searches Wikipedia for a specific topic and returns the page content.
        Args:
            topic: The title of the page (e.g., "Artificial Intelligence", "Elon Musk")
        """
        my_order = {
	         "action": "query",
	         "format": "json",
	         "prop": "extracts",
	         "titles": topic,
	        "formatversion": "2",
	        "exlimit": "1",
	        "explaintext": 1
       }


        headers = {"User-Agent": "ManjunadhaRAG/1.0 (learning; contact: manjunadha231@gmail.com)"}
        response = requests.get(url=wikiurl,headers=headers, params=my_order)
        final = response.json()
        ans = final["query"]["pages"][0]["extract"]
        return ans



def ask_llm(question):

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """
            You are a Fact-Checking Agent.
            
            Your Goal: Fetch facts using the 'search' tool and format them.
            
            CRITICAL RULES:
            1. You MUST use the 'search' tool for EVERY question.
            2. You are FORBIDDEN from answering from memory.
            3. If you did not use the tool, you must output "source_verified": false.
            
            OUTPUT SCHEMA (Strict JSON):
            {{
              "answer": "Concise answer based on the tool output.",
              "source_verified": true, 
              "source_name": "Wikipedia",
              "supporting_quotes": ["Short quote 1", "Short quote 2"],
              "confidence": "high|low"
            }}
            """),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        user_data = f"question: {question}"
        llm = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-2.0-flash")
        tools = [search]
        agent = create_tool_calling_agent(llm, tools, prompt=prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        response = agent_executor.invoke({"input": user_data})

        raw_output = response["output"]
        clean_output = raw_output.replace("```json", "").replace("```", "").strip()
        return clean_output
        

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        answer = ask_llm(request.question)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=8000)
        

        

    
         
        