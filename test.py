import asyncio

from search import Agent


async def main():
    agent = Agent(input("ask me anything: "), max_searches=5)

    async for res in agent.start():
        if res.type == "ai":
            print("\r[2K(ai) ", res.text[:100].strip('```').replace("\n", " "), end="")

        elif res.type == "searcher":
            print("\r(searcher) \x1b[2m", res.searcher.format()[:100].replace("\n", " "), end="\x1b[0m")

        elif res.type == "thoughts":
            print("\r(thoughts) \x1b[2m", (res.thoughts or "none")[:100], end="\x1b[0m")

        elif res.type == "summarization":
            print("\n\n\x1b[1mSummarization:\n" + res.summarization, end="\x1b[0m\n")

        elif res.type == "error":
            pass  # lmaoooo


asyncio.run(main())
