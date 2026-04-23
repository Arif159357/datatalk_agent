def get_chat_history(chat_history):
    history_text = ""
    for msg in chat_history:
        role = "User" if msg.type == "human" else "Assistant"
        history_text += f"{role}: {msg.content}\n"

    return history_text
