import json
from .escape_markdown_v2 import escape_md_v2


def parse_context(data: dict) -> str:
    if not data:
        return "```json\n{}\n```"
    
    try:
        formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
        escaped_json = escape_md_v2(formatted_json)
        return f"```json\n{escaped_json}\n```"
    except Exception:
        parsed_str = ""
        for key, value in data.items():
            parsed_str += f"{escape_md_v2(str(key))}: {escape_md_v2(str(value))}\n"
        return f"```{parsed_str}```"