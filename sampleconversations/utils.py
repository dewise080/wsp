from datetime import datetime, timedelta
from typing import Iterable, Mapping


def _format_timestamp(dt: datetime) -> str:
    # WhatsApp export style: 02/12/24, 7:08 PM
    return dt.strftime("%d/%m/%y, %I:%M %p").lstrip("0")


def build_whatsapp_text(
    conversations: Iterable[Mapping],
    user_name: str = "Author",
    assistant_name: str = "Assistant",
    start: datetime | None = None,
    minute_step: int = 1,
) -> str:
    """
    Convert a list of conversation dicts into WhatsApp-style plaintext
    with synthetic timestamps and author names.
    """
    base = start or datetime(2024, 12, 2, 19, 0)
    lines: list[str] = []
    current = base

    for convo in conversations or []:
        user_msg = (convo.get("user_message") or "").strip()
        assistant_msg = (convo.get("assistant_message") or "").strip()

        if user_msg:
            lines.append(f"{_format_timestamp(current)} - {user_name}: {user_msg}")
            current += timedelta(minutes=minute_step)

        if assistant_msg:
            lines.append(f"{_format_timestamp(current)} - {assistant_name}: {assistant_msg}")
            current += timedelta(minutes=minute_step)

    return "\n".join(lines)
