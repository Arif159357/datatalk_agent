from langchain_classic.memory.summary_buffer import ConversationSummaryBufferMemory
from llms.chat_models import gemini

memory_summary = ConversationSummaryBufferMemory(
    memory_key="chat_history",
    llm=gemini,
    output_key="output",
    return_messages=True,
)
