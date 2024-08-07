# cheapest-search
Here we have the cheapest search engine to ever exist, with Groq.

**Key features**:
- Search on the internet like a human
- Async-based
- Faster with Groq®️


This project is not yet installable via `pip`, but it will be supported sooner (I assume). For now, use `git clone` to clone this project and make it yours.

```python
from search import pipeline

await pipeline(
    "who invented planes?",
    max_searches=5,  # for faster results, 5-10 is a good range
    verbose=True     # what the ai doin'?????
)
```


<img 
    src="https://i.ytimg.com/vi/rqvA7T5FUTQ/maxresdefault.jpg"
    align="center"
/>

## 🤯 Demo
This emoji is cringe.

https://raw.githubusercontent.com/AWeirdDev/cheapest-search/assets/demo.mp4

## 🐣 Essentials
Yo is that Chick Fil-a? Anyway, let's see what we need to do first. That is:
- Install packages
- Get your [Groq](https://console.groq.com) API key
- Configure Groq

## Install Packages
Install everything! Don't worry, we strive to keep everything minimal. All you need is the `groq` and my custom `researches` package.

```bash
pip install -r requirements.txt
# or:
pip install -U groq researches
```

> [!NOTE]
> `httpx` comes along with `groq` or `researches`, so you don't need to install it separately.

### Configuring Groq
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

# Support awdev
Support this project (and quite possibly, support me) by donating!

[☕ Buy me a coffee!](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAs_TDUTeHiZQ1tqLJlvItaBOjcmRTeoSbHw&s)

nya ichi ni san

***

(c) 2024 AWeirdDev