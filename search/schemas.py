from dataclasses import dataclass
from typing import Literal, Optional

from .searcher import Searcher


@dataclass
class Usage:
    """The usage statistics for the response.

    Attributes:
        completion_token (int): The number of completion tokens.
        prompt_tokens (int): The number of prompt tokens.
    """

    type: Literal["usage"]
    completion_token: int
    prompt_tokens: int


@dataclass
class Thoughts:
    """The AI's thoughts before an action.

    Attributes:
        thoughts (str, optional): The AI's thoughts.
    """

    type: Literal["thoughts"]
    thoughts: Optional[str]


@dataclass
class SearcherResponse:
    """The response from the searcher.

    Attributes:
        searcher (Searcher): The searcher.
    """

    type: Literal["searcher"]
    searcher: Searcher


@dataclass
class Summarization:
    """The summarization of the search.

    Attributes:
        summarization (str): The summarization.
    """

    type: Literal["summarization"]
    summarization: str


@dataclass
class AIResponse:
    """The response from the AI.

    Attributes:
        text (str): The AI's response.
    """

    type: Literal["ai"]
    text: str


@dataclass
class Error:
    """Represents an error during the search.

    Attributes:
        error (str): The error message.
        would_retry (bool): Whether to retry.
    """

    type: Literal["error"]
    error: str
    would_retry: bool
