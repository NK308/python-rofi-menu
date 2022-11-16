import json
import base64
import os
import sys
from typing import Optional


def get_env() -> tuple[str, Optional[str], Optional]:
    RETV = os.env.get("ROFI_RETV")
    INFO = os.env.get("ROFI_INTO")
    DATA = os.env.get("ROFI_DATA")
    if INFO is not None:
        INFO = base64.decode(INFO).decode("utf-8")
    if DATA is not None:
        DATA = json.loads(base64.decode(DATA).decode("utf-8"))
    return RETV, INFO, DATA


def get_line() -> str:
    return sys.argv[1]


def decode_script_input() -> tuple[str, Optional, Optional[str], Optional[str]]:
    RETV, INFO, DATA = get_env()
    if RETV == 0:
        ACTION = "INITIAL_CALL"
    elif RETV == 1:
        ACTION = "ENTRY_SELECTED"
    elif RETV == 2:
        ACTION = "CUSTOM_ENTRY"
    else:
        ACTION = f"CUSTOM_KEY_{int(RETV)-9}"
    if not ACTION == "INITIAL_CALL":
        line = get_line()
    else:
        line = None
    return ACTION, DATA, INFO, line

