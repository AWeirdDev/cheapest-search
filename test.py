import asyncio

from search import Agent


async def main():
    agent = Agent(input("\x1b[2mask me anything: \x1b[0m\x1b[33m"), max_searches=5)
    print("\x1b[0m", end="")

    async for res in agent.start():
        if res.type == "searcher":
            print("\r(searcher) \x1b[2m", res.searcher.format()[:100].replace("\n", " "), end="\x1b[0m")

        elif res.type == "thoughts":
            print("\r(thoughts) \x1b[2m", (res.thoughts or "none")[:100], end="\x1b[0m")

        elif res.type == "summarization":
            print("\n\n\x1b[1mSummarization\x1b[0m:\n" + res.summarization, end="\n")

        elif res.type == "error":
            pass  # lmaoooo


asyncio.run(main())
