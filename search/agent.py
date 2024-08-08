"""Search agent."""

from typing import AsyncGenerator, Dict, List, Optional, Union

from . import schemas as S

from .ai import _d
from .formatter import Formatter
from .prompt import get_prompt
from .searcher import Searcher

Schemas = Union[
    S.Usage,
    S.AIResponse,
    S.Thoughts,
    S.SearcherResponse,
    S.Summarization,
    S.Error,
]
AgentGeneratorResponse = AsyncGenerator[
    Schemas,
    None,
]


class Agent:
    """Represents the AI agent for search tasks.

    Example:
    .. code-block :: python

        agent = Agent("taiwan gdp")
        async for res in agent.start():
            if res.type == "summarization":
                print(res.summarization)
    """

    __slots__ = ("query", "messages", "max_searches", "cap")
    query: str
    messages: List[Dict[str, str]]
    max_searches: int

    def __init__(self, query: str, *, max_searches: int = 10, cap: int = -1):
        """Initializes the agent.

        Args:
            query (str): The search query.
            max_searches (int, optional): The maximum number of searches. Defaults to 10.
                Provide ``-1`` for unlimited. **This may result in a slow response and high cost.**
            cap (int, optional): ``A = max_searches + cap - 1`` thus the cap should be negative/zero.
                When the message count is equal/above ``A``, the agent will be reminded to be faster.
        """
        assert cap <= 0, "Cap should be negative/zero."
        self.query = query
        self.messages = []
        self.max_searches = max_searches
        self.cap = cap

    async def start(
        self,
    ) -> AgentGeneratorResponse:
        """Starts the agent."""
        # add the query first
        self.messages.append({"role": "user", "content": "QUERY " + self.query})

        groq = _d.groq

        i = 0
        while i < 10:
            res = await groq.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": get_prompt("light")},
                    *self.messages,  # type: ignore
                ],
            )
            content = res.choices[0].message.content
            assert (
                content
            ), "No content in response (internal error: status.groq.com), or retry."

            if res.usage:
                yield S.Usage(
                    "usage", res.usage.completion_tokens, res.usage.prompt_tokens
                )

            fmt = Formatter(content)
            self.messages.append({"role": "assistant", "content": fmt.response})

            yield S.AIResponse("ai", fmt.response)

            yield S.Thoughts("thoughts", fmt.thoughts)

            if fmt.query:
                # AI sent a query
                searcher = await Searcher(fmt.query).future()
                result_text = searcher.format()

                # Get reminders (e.g., ai forgot to add steps)
                reminder = fmt.get_reminder(
                    near_overflow=i == self.max_searches - 1 + self.cap
                )

                self.messages.append(
                    {"role": "user", "content": "SYSTEM\n" + result_text + reminder}
                )
                yield S.SearcherResponse("searcher", searcher)

            elif fmt.summarization:
                yield S.Summarization("summarization", fmt.summarization)
                return

            else:
                self.messages.pop(-1)
                yield S.Error(
                    "error",
                    "The AI did not provide anything correctly. Retrying.",
                    True,
                )
                continue

            i += 1

        yield S.Error(
            "error",
            "[CRITICAL] Failed to summarize before the limit.",
            False,
        )

    def __aiter__(self) -> "Agent":
        return self

    async def __anext__(self) -> Schemas:
        return await self.start().__anext__()

    async def answer(self) -> str:
        """Fetches the answer."""
        async for res in self:
            if res.type == "summarization":
                return res.summarization
            elif res.type == "error" and not res.would_retry:
                raise RuntimeError(f"Unexpected response type: {res.type}")

        raise RuntimeError("Failed to summarize before the limit.")


async def pipeline(
    query: str, *, max_searches: int = 10, cap: int = -1, verbose: bool = True
) -> Optional[str]:
    """Represents the search pipeline. Designed for simplicity.

    Args:
        query (str): The search query.
        max_searches (int, optional): The maximum number of searches. Defaults to 10.
            Provide ``-1`` for unlimited. **This may result in a slow response and high cost.**
        cap (int, optional): ``A = max_searches + cap - 1`` thus the cap should be negative/zero.
            When the message count is equal/above ``A``, the agent will be reminded to be faster.
        verbose (bool, optional): Whether to print the response. Defaults to True.
    """
    agent = Agent(query, max_searches=max_searches, cap=cap)

    def vprint(*args):
        if verbose:
            print(*args)

    async for res in agent.start():
        if res.type == "error":
            if res.would_retry:
                vprint("(skipped) error:", res.error)
            else:
                raise RuntimeError(res.error)

        elif res.type == "summarization":
            vprint("summarization:\n ", res.summarization)
            return res.summarization

        else:
            vprint(res)
