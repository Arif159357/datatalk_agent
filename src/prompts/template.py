from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage

from llms.chat_models import gemini
from database.database import datatalk_db
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from prompts.sql_system import sql_system_prompt
from database.vector import get_full_schema_as_string


sql_toolkit = SQLDatabaseToolkit(db=datatalk_db, llm=gemini)


def get_prompt_template():
    sys_prompt = sql_system_prompt.format(dialect=sql_toolkit.dialect,
                                          dynamic_schema=get_full_schema_as_string())


    sys_msg = SystemMessage(content=sys_prompt)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            sys_msg,
            MessagesPlaceholder("chat_history"),
            HumanMessagePromptTemplate.from_template(template="{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    return prompt_template
