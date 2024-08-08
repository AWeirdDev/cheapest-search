# cheapest-search
Here we have the cheapest search engine to ever exist, with Groq. Only PERP fans would understand this.

**Key features**:
- Search on the internet like a human
- Async-based
- Faster with Groq®️


This project is not yet installable via `pip`, but it will be supported sooner (I assume). For now, use `git clone` to clone this project and make it yours.

> Beware of Google blocks. You might get blocked for a while if there are mass requests.

```python
from search import pipeline

await pipeline(
    "who invented planes?",
    max_searches=5,  # for faster results, 5-10 is a good range
    verbose=True     # what the ai doin'?????
)
```

https://github.com/user-attachments/assets/59d7d77e-2809-444e-aa2c-96c6897723c3

## 🐣 Essentials
Yo is that Chick Fil-a? Anyway, let's see what we need to do first. That is:
- Clone this project
- Install packages
- Get your [Groq](https://console.groq.com) API key
- Configure Groq

### i. Cloning
Clone this project with `git`:
```bash
git clone https://github.com/AWeirdDev/cheapest-search
cd cheapest-search
```


### ii. Install Packages
Install everything! Don't worry, we strive to keep everything minimal. All you need is the `groq` and my custom `researches` package.

```bash
pip install -r requirements.txt
# or:
pip install -U groq researches
```

> [!NOTE]
> `httpx` comes along with `groq` or `researches`, so you don't need to install it separately.

### iii. Configuring Groq
[Get an API key](https://console.groq.com) first.

We have two ways to configure Groq, yet it's always recommended to use a virtual environment.

<details>
<summary>

With virtual environment (`pipenv`, `venv`, ...)

</summary>

1. Setup your virtual environment. Here, we'll use `pipenv` as it's easy to setup with Visual Studio Code:

```bash
pip install pipenv
pipenv --python 3.x  # "x" is your python version (e.g., 3.12)
```

2. Press <kbd>⌘ Command (ctrl)</kbd> <kbd>shift</kbd> <kbd>P</kbd> and type "select interpreter," then select your virtual environment.
3. Add a `.env` in the working directory and add your Groq API key:
```ini
GROQ_API_KEY=uwu
```

4. Refresh your terminal to load the environment.

</details>

<details>
<summary>

Add your API key responsibly just like Rabbit R1 or use `os.environ`

</summary>

There's a quick method available, yet you'll need to configure your own `AsyncGroq` class:
```python
from groq import AsyncGroq
from search import configure_groq

configure_groq(
    AsyncGroq(
        api_key="xxxx"  # ...or use os.environ
    )
)

# ...do stuff
```

</details>


## 🥳 Use
For people who want it to try out, you can use `pipeline()` to be more clear of the usage. If you want to handle your own, use the `Agent` class.

### pipeline
For quick starters, use `pipeline` to get the result quickly.
```python
import asyncio
from search import pipeline

async def main():
    await pipeline(
        "who invented papers?",
        max_searches=5,
        cap=-2,  # when 3 messages left, we'll remind groq to be faster!
        verbose=True  # get details behind the scenes
    )

asyncio.run(main())
```

### Agent
```python
import asyncio
from search import Agent

async def main():
    agent = Agent(
        "what's the song never gonna give you up about",
        max_searches=5,
    )

    async for res in agent.start():
        if res.type == "ai":
            # AI's response
            print(res.text)

        elif res.type == "usage":
            print(res.completion_token)
            print(res.prompt_tokens)

        elif res.type == "searcher":
            # Searcher response (from google search)
            print(res.searcher)

        elif res.type == "thoughts":
            # AI's thoughts before an action
            print(res.thoughts)

        elif res.type == "summarization":
            # AI's summary (done)
            print(res.summarization)
            break

        elif res.type == "error":
            # Error
            print(res.error, res.would_retry)

    print("done!")

asyncio.run(main())
```

## How it works
We look for information. We search. We extract data. This explains that we humans do when we hop on search engines: to look for the exact piece of information we want! However, sometimes we can't quite see the whole picture: data is everywhere, and considering the average attention we'd all skip for everything and say "i aint reading allat."

What if we let an AI do it? They'll read the data, extract them and generate a brief summary. Isn't that just faster and easier? Plus, if we used Groq, everything is sped up 2-4x!

Let's say we want to search the song "slow dancing in the dark," and we don't know what it's about.

The LLM extracts it, and makes sure what it wants to do.

> **Llama 3** <kbd>AI</kbd>
> 
> ```yaml
> # steps: I should look it up using "search." I should specify the wording "song" in my query otherwise I might get information on a different topic.
> search: joji slow dancing in the dark song
> ```

As you can see, the AI is aware of what they should be searching, thanks to the "# steps" comment, making the AI more clear of the context.

We then parse the response, format the grammar to meet our requirements, and search it on the web with `researches`.

Repeat the loop, and we can get fascinating results!

## Questions
It's funny, no one has ever "frequently" asked those questions from the FAQs if you really think about it.

**What does this differ from MindSearch?**<br />
MindSearch is made in China and this is made in Taiwan. To be more explicit, this project strives to keep everything simple since extra dependencies are always frustrating!

**Is there an API documentation?**<br />
I'll consider making one. [Issues](https://github.com/AWeirdDev/cheapest-search/issues/new?title=gimme+gimme+docs)

**How can I get started?**<br />
Read the "Use" category above.

# Donate
Support this project (and quite possibly, support me) by donating!

[☕ Buy me a coffee!](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAs_TDUTeHiZQ1tqLJlvItaBOjcmRTeoSbHw&s)

nya ichi ni san

***

(c) 2024 AWeirdDev
