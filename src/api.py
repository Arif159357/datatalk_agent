import re
import io
import base64
import matplotlib.pyplot as plt
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Import your existing components
from agents.sql_agent.agent import SQLAgentManager
from memory.chat_history import get_chat_history
from memory.chat_memory import memory_summary


# Models for request/response
class QueryRequest(BaseModel):
    question: str
    session_id: str

class VisualizationData(BaseModel):
    image_base64: Optional[List[str]] = None

class QueryResponse(BaseModel):
    answer: Optional[str] = None
    visualization: Optional[VisualizationData] = None

# Store active sessions
sessions = {}
session_agents = {}
session_visualizations = {}


# Helper functions for visualization
def extract_python_code(text):
    """Extract Python code blocks from text"""
    pattern = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)
    code_blocks = pattern.findall(text)
    return code_blocks


def generate_plot(code_blocks):
    """Generate visualization from Python code blocks and return as base64 images"""
    try:
        # Create a list to store multiple images
        image_base64_list = []

        # Process each code block
        for code in code_blocks:
            # Get the current figure count before executing this code block
            initial_fig_count = plt.get_fignums()

            # Execute the Python code
            exec(code)

            # Get all figures created by this code block
            final_fig_count = plt.get_fignums()

            # Process each figure created by this code block
            for fig_num in final_fig_count:
                if fig_num not in initial_fig_count:
                    # Select the figure
                    fig = plt.figure(fig_num)

                    # Save the plot to a bytes buffer
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png")
                    buf.seek(0)

                    # Convert to base64
                    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                    image_base64_list.append(image_base64)

            # Close all figures after processing this code block
            plt.close("all")

        return {"image_base64": image_base64_list}
    except Exception as e:
        plt.close("all")
        print(f"Plot generation error: {str(e)}")
        return {
            "image_base64": [""]
        }  # Return list with empty string to avoid validation error


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize any resources
    print("Starting up Analytics API...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down Analytics API...")
    sessions.clear()


# Initialize FastAPI app
app = FastAPI(
    title="Analytics Agent API",
    description="API for querying data with an analytical agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query against the database

    Args:
        request: Contains the question and optional session_id

    Returns:
        Query results including answer, SQL, and visualization if applicable
    """
    try:
        visualization = None
        visualization_list = []
        # Create or retrieve memory
        if request.session_id and request.session_id in sessions:

            memory_obj = sessions[request.session_id]
            chat_history = get_chat_history(memory_obj.chat_memory.messages)
            if request.session_id in session_visualizations:
                visualization_list = session_visualizations[request.session_id]
            else:
                visualization_list = []
                session_visualizations[request.session_id] = visualization_list
        else:
            memory_obj = memory_summary
            chat_history = get_chat_history(memory_obj.chat_memory.messages)
            if request.session_id:
                sessions[request.session_id] = memory_summary

        # Create or retrieve agent for this session
        if request.session_id and request.session_id in session_agents:
            agent = session_agents[request.session_id]
            agent.memory = memory_obj  # Ensure memory is up to date
        else:
            agent = SQLAgentManager(memory_obj)
            if request.session_id:
                session_agents[request.session_id] = agent

        # Execute query with session-specific agent
        result = agent.query(request.question, chat_history)
        # Extract visualization if present
        try:
            if isinstance(result, list):
                answer_text = result[0]['text']
            elif "Agent stopped due to max iterations" in result:
                answer_text = "Could you please rewrite your question with a bit more detail or clarify what you're looking for?"
            else:
                answer_text = result

            print("answer_text: ", answer_text)
            code_blocks = extract_python_code(answer_text)
            print("code_blocks: ", len(code_blocks), code_blocks)

            if code_blocks:
                plot_result = generate_plot(code_blocks)
                visualization_list = plot_result["image_base64"]
                visualization = VisualizationData(
                    image_base64=visualization_list,
                )
        except Exception as e:
            print(e)
            raise e
        # Format response
        if visualization:
            last_message = memory_obj.chat_memory.messages[-1].content

            if isinstance(last_message, list):
                last_message = last_message[0]
                if isinstance(last_message, dict):
                    last_message = last_message['text']

            # Replace the Python code block with the image data
            image_message = "[IMAGE_DATA:]"
            modified_message = re.sub(
                r"```python\s*\n.*?```",
                image_message,
                last_message,
                flags=re.DOTALL,
            )
            # Remove the old message and add the modified one
            memory_obj.chat_memory.messages.pop()
            memory_obj.chat_memory.add_ai_message(modified_message)

            sessions[request.session_id] = memory_obj
            session_visualizations[request.session_id] = visualization_list

            return QueryResponse(
                answer=modified_message,
                visualization=visualization,
            )
        else:
            sessions[request.session_id] = memory_obj
            return QueryResponse(
                answer=answer_text,
                visualization=None,
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Query processing failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
