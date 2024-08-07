import re


class Formatter:
    """Represents the response grammar formatter."""

    __slots__ = (
        "raw",
        "forgot_steps",
        "response",
        "thoughts",
        "query",
        "summarization",
    )

    def __init__(self, raw: str):
        """Initialize the formatter.

        Args:
            raw (str): The raw response.
        """
        self.raw = raw
        self.forgot_steps = False
        self.thoughts = None
        self.query = None
        self.summarization = ""

        self.fix_grammar(raw)
        self.parse()

    def fix_grammar(self, response: str) -> None:
        """Fix the response grammar.

        Args:
            response (str): The raw response.
        """

        if (
            response.startswith("```")
            and not response.endswith("```")
            and response.count("```") == 1
        ):
            # print("alignment 0")
            response += "\n```"

        if (
            not response.startswith("```")
            and "```" in response
            and not response.endswith("```")
        ):
            # print("alignment 1")
            response = re.findall(
                r"```(?:yaml|yml)?\n(.+)", response, re.MULTILINE | re.S
            )[0]
            response = "```\n" + response.strip() + "\n```"

        if not response.startswith("```") and response.endswith("```"):
            # print("alignment 2")
            response = re.findall(
                r"```(?:yaml|yml)?\n(.+)```", response, re.MULTILINE | re.S
            )[0]
            response = "```\n" + response.strip() + "\n```"

        if response.count("```") >= 2:
            # print("alignment 3")
            response = re.findall(
                r"```(?:yaml|yml)?\n(.+?)```", response, re.MULTILINE | re.S
            )[0]
            response = "```\n" + response.strip() + "\n```"

        self.response = response

    def parse(self):
        """Parse the response.

        This is automatically emitted on ``__init__()``.
        """
        lines = self.response.strip("```").strip().splitlines()

        i = 0
        state = None

        while i < len(lines):
            line = lines[i]

            if not state:
                if line.startswith("# steps: "):
                    self.thoughts = line[len("# steps: ") :]

                elif line.startswith("search: "):
                    self.query = line[len("search: ") :]

                elif line.startswith("summarization:"):
                    state = "summarization"
                    self.summarization += line[len("summarization:") :].strip() + "\n"

            elif state == "summarization":
                self.summarization += line + "\n"

            i += 1

    def get_reminder(self, *, near_overflow: bool = False) -> str:
        """Get the reminder.

        Args:
            near_overflow (bool): If the search maximum search capacity is near.
        """
        p = []

        if not self.thoughts:
            p.append('- You did not provide "# steps" (CRUCIAL)')

        if near_overflow:
            p.append(
                "- YOU ARE RUNNING OUT OF SEARCHES. FINISH THE SEARCH WITH summarization NOW."
            )

        return ("WARNING:\n" + "\n".join(p)) if p else ""
