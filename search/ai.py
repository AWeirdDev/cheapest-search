from groq import AsyncGroq


class _d:
    """dummy object to hold the groq client.

    lol don't judge me. it works.
    """

    groq = AsyncGroq()


def configure_groq(g: AsyncGroq) -> None:
    """Config the ``groq`` variable instead of the default one because why not.

    Args:
        q (AsyncGroq): Groq client. Must be **async**.
    """
    _d.groq = g
