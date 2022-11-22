from .rofi_mode import RofiMode


def get_rofi_mode(version: str) -> RofiMode:
    ver = tuple(int(part) for part in version.split("."))

    if ver >= (1, 7, 4):
        from . import rofi_mode_174
        return rofi_mode_174.RofiMode()

    elif ver >= (1, 6):
        from . import rofi_mode_16

        return rofi_mode_16.RofiMode()
    else:
        from . import rofi_mode_15
        return rofi_mode_15.RofiMode()


    raise RuntimeError("Wrong version configuration")
