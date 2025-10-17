import json
from collections.abc import Mapping
from typing import Any

from loggertgnotifier.helpers.escape_markdown_v2 import escape_md_v2


def parse_context(data: Mapping[str, Any] | None) -> str:
    if not data:
        return "```json\n{}\n```"

    try:
        formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
        escaped_json = escape_md_v2(formatted_json)
        return f"```json\n{escaped_json}\n```"
    except Exception:
        parsed_lines = [
            f"{escape_md_v2(str(key))}: {escape_md_v2(str(value))}"
            for key, value in data.items()
        ]
        parsed_str = "\n".join(parsed_lines)
        return f"```{parsed_str}```"
