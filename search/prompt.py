"""Simple prompt loader."""

from typing import Dict


__prompts__: Dict[str, str] = {}


def load_prompt(name: str):
    with open("_prompts/" + name + ".md", encoding="utf-8") as f:
        __prompts__[name] = f.read()


def get_prompt(name: str) -> str:
    if name not in __prompts__:
        load_prompt(name)

    return __prompts__[name]
