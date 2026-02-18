"""
Types for the project.
"""

__all__: list[str] = [
    "JsonType",
]

# NOTE: This module is only used if you wants to add types to the project.
# If you don't need types, you can remove this module.
# Here is an example of a type:

type JsonType = None | int | str | bool | list[JsonType] | dict[str, JsonType]
"""
JSON types.

This is a union of all possible JSON types.
"""
