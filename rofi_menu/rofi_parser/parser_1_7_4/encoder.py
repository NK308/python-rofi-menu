import json
import base64
import sys
from typing import Optional


def create_header_line(key: str, value: str) -> str:
    if key == "data":
        value = base64.encode(value.encode("utf-8"))
    return f"\0{key}\x1f{value}"


def create_header(mode_options: dict[str, str]) -> str:
    return "\n".join([create_header_line(k, v) for k, v in mode_options.items()])


def create_row_option(key: str, value: str) -> str:
    if key == "info":
        value = base64.encode(value.encode("utf-8"))
    return f"{key}\x1f{value}"


def create_row(value: str, row_options: Optional[dict[str, str]]) -> str:
    if row_options is not None:
        options = "\x1f".join([create_row_option(k, v) for k, v in row_options.items()])
    else:
        options = ""
    line = value.replace("\n", "   ")
    if not options == "":
        line = f"{line}\0{options}"
    return line

def generate_output(entries: list[tuple[str, Optional[dict[str, str]]]], header_options: Optional[dict[str, str]] = None):
    if header_options is not None:
        header = create_header(header_options)
    else:
        header = ""
    rows = "\n".join([create_row(line, options) for line, options in entries])
    if header == "":
        return rows
    elif rows == "":
        return header
    else:
        return f"{header}\n{rows}"


