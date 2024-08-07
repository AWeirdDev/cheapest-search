"""Represents the searcher."""

from typing import Optional

from researches import asearch
from researches.schemas import Result


class Searcher:
    """Represents a searcher.

    This is a simple wrapper for ``researches``.

    Example:
    .. code-block :: python

        searcher = await Searcher("taiwan gdp").future()
        print(searcher.format())
    """

    __slots__ = ("q", "res")
    q: str
    res: Optional[Result]

    def __init__(self, q: str):
        """Initialize a searcher.

        Args:
            q (str): The search query.
        """
        self.q = q
        self.res = None

    async def future(self) -> "Searcher":
        """Perform the search.

        Can be used with chains.

        Returns:
            :obj:`Searcher`: The searcher.
        """
        self.res = await asearch(self.q)
        return self

    def format(self) -> str:
        """Formats the search result for LLM consumption.

        Returns:
            str: The formatted result.
        """
        assert self.res, "Post init must be done first. Use `await searcher.future()`"

        res = self.res
        contents = []

        if res.snippet:
            contents.append(
                "Quick answer:\n"
                + (
                    res.snippet.highlighted
                    if res.snippet.highlighted
                    else res.snippet.text
                )
            )

        if res.aside and res.aside.text:
            contents.append("Aside:\n" + res.aside.text)

        if res.flights:
            contents.append(
                "Flights:\n"
                + "title description duration price"
                + "\n".join(
                    {
                        f"{flight.title} {flight.description} {flight.duration} {flight.price}"
                        for flight in res.flights
                    }
                )
            )

        if res.lyrics:
            contents.append(
                "Lyrics:\n"
                + res.lyrics.text
                + (" (search to view more)" if res.lyrics.is_partial else "")
            )

        if res.weather:
            now = res.weather.now
            contents.append(
                "Weather:\n"
                + (
                    "Now:\n"
                    + f"{now.c}C {now.f}F, "
                    + f"{now.description}\n"
                    + f"humidy: {now.humidity}, precipitation: {now.precipitation}\n"
                    + f"wind: {now.wind_metric} / {now.wind_imperial}"
                )
                + "Forecast:\n"
                + "\n".join(
                    [
                        f"{fc.weekday} high: {fc.high_c}/{fc.high_f}, low: {fc.low_c}/{fc.low_f}"
                        for fc in now.forecast
                    ]
                )
                + (("Warning:\n" + res.weather.warning) if res.weather.warning else "")
            )

        if len(contents) < 2:
            contents.append(
                "Web:\n"
                + "\n".join(
                    [
                        f"{w.title}\n{w.text}\n{w.url.split('://', 1)[1].split('/')[0]}\n"
                        for w in res.web
                    ]
                )
            )

        return "\n".join(contents)
