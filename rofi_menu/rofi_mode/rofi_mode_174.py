"""
Rofi script mode for version >=174
"""
import base64
import json
import os
from typing import Optional

ROFI_RETV_INITIAL_SCRIPT_CALL = "0"
ROFI_RETV_SELECTED_ENTRY = "1"
ROFI_RETV_CUSTOM_ENTRY = "2"


class RofiMode:
    def render_menu(self, *items: str) -> str:
        return "\n".join(items)

    def menu_global_meta(self, global_meta):
        return f"\0data\x1f{base64.urlsafe_b64encode(json.dumps(global_meta))}"

    def menu_prompt(self, text: str) -> str:
        return f"\x00prompt\x1f{text}"

    def menu_enable_markup(self) -> str:
        return "\0markup-rows\x1ftrue"

    def menu_message(self, text: str) -> str:
        return f"\0message\x1f{text}"

    def menu_urgent(self, num: int) -> str:
        return f"\0urgent\x1f{num}"

    def menu_active(self, num: int) -> str:
        return f"\0active\x1f{num}"

    def menu_no_input(self, val: bool = True) -> str:
        return "\0no-custom\x1f" + ("true" if val else "false")

    def _menu_entry(self, text, **fields):
        if not fields:
            return text

        fields_data = "\x1f".join([f"{name}\x1f{val}" for name, val in fields.items()])
        return f"{text}\x00{fields_data}"

    def menu_item(
        self,
        text: str,
        icon: Optional[str] = None,
        searchable_text: Optional[str] = None,
        nonselectable: Optional[bool] = None,
        meta_data: Optional[dict] = None,
    ) -> str:

        fields = {}

        if icon is not None:
            fields["icon"] = icon

        if searchable_text is not None:
            fields["meta"] = searchable_text

        if nonselectable is not None:
            fields["nonselectable"] = "true" if nonselectable else "false"

        info = base64.urlsafe_b64encode(json.dumps(meta_data).encode("utf-8")).decode(
            "utf-8"
        )
        fields["info"] = info

        return self._menu_entry(text, **fields)

    def parse_meta(self, selected_item: str) -> dict:
        rofi_retv = os.getenv("ROFI_RETV")
        rofi_info = os.getenv("ROFI_INFO")
        rofi_data = os.getenv("ROFI_DATA")

        if rofi_retv != ROFI_RETV_INITIAL_SCRIPT_CALL and rofi_data:
            meta = json.loads(base64.urlsafe_b64decode(rofi_data))
        else:
            meta = {}
        if rofi_retv == ROFI_RETV_INITIAL_SCRIPT_CALL:
            meta["ACTION"] = "INITIAL_SCRIPT_CALL"
        elif rofi_retv == ROFI_RETV_SELECTED_ENTRY:
            meta["ACTION"] = "ENTRY_SELECTED"
        elif rofi_retv == ROFI_RETV_CUSTOM_ENTRY:
            meta["ACTION"] = "CUSTOM_ENTRY"
        else:
            meta["ACTION"] = f"CUSTOM_KEY_{int(rofi_retv) - 9}"
        if rofi_info:
            meta["ITEM_META"] = json.loads(base64.urlsafe_b64decode(rofi_info))
        return {}
