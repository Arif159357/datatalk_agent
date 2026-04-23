def get_full_schema_as_string() -> str:
    with open("./database/datatalk.md", 'r', encoding='utf-8') as f:
        full_schema_string = f.read()

    return full_schema_string
