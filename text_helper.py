"""
Various utilities for parsing text.
"""
from typing import Optional, Tuple, Union

def parse_name(full_name: str) -> Union[Tuple[str, Optional[str]], Tuple[None, None]]:
    """
    Split the full name into first and last names.
    The last name will be everything after the first
    space.
    This does not handle titles and degrees, e.g.
    "Mrs. Barbara Smith DDS".
    """
    if not full_name:
        return None, None

    name_parts = full_name.split(" ", maxsplit=1)
    return name_parts[0], name_parts[1] if len(name_parts) > 1 else None
