from langchain_community.agent_toolkits import create_sql_agent
from datetime import datetime, timezone

from prompts.template import sql_toolkit
from prompts.template import get_prompt_template
from prompts.paraphraser import paraphraser_system_prompt
from database.vector import get_full_schema_as_string
from llms.functions import call_model


class SQLAgentManager:
    def __init__(self, memory):
        self.sql_toolkit = sql_toolkit
        self.memory = memory
        self.model_name = "google"
        self.prompt_template = get_prompt_template()
        self.agent = self._build_prompt()

    def _build_prompt(self):
        return create_sql_agent(
            llm=self.sql_toolkit.llm,
            toolkit=self.sql_toolkit,
            agent_type="tool-calling",
            verbose=True,
            prompt=self.prompt_template,
            agent_executor_kwargs={
                "memory": self.memory,
                "return_intermediate_steps": True,
                "output_key": "output",
            },
        )

    def generate_refined_question(self, user_question, conversation_history):
        """
        Calls the "Query Analyst" LLM to refine the user's question.
        """
        current_time = datetime.now(timezone.utc).isoformat()
        schema = get_full_schema_as_string()

        sys_prompt = f"""{paraphraser_system_prompt}

        ## Technical Schema (for SQL generation) ##
        {schema}
        """
        user_prompt = f"""

        **## Conversation History ##**
        {conversation_history}

        # **## New User Question ##**
        # {user_question}

        **## Refined Question ##**
        """
        try:
            response_text = call_model("google", user_prompt, sys_prompt)
        except Exception as e:
            print(e)

        return response_text

    def query(self, question: str, chat_history: str) -> str:
        try:
            refine_question = self.generate_refined_question(
                question, chat_history
            )
            print("User question:", question)
            print("Refined question:", refine_question)
            result = self.agent.invoke({"input": refine_question})
            answer = result["output"]
            graph_triggers = ["graph", "plot", "chart", "diagram", "visualize"]
            if any(word in question.lower() for word in graph_triggers):
                print("Generating visualization code...")
                viz_prompt = f"""
                The user wants a visualization for this data: {answer}
                Based on the question: {question}
                Generate ONLY a Python matplotlib code block.
                Ensure the code uses 'plt.figure()' and does not use 'plt.show()'.
                Format: ```python ... ```
                """
                python_code = call_model("google", viz_prompt, "You are a data visualization expert.")
                answer[0]['text'] += "\n\n" + python_code
            
            print("Answer:", answer)
        except Exception as e:
            print(e)
        return answer
