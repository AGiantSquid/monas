from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from rich.prompt import Prompt

from mono.utils import console


@dataclass
class Question:
    """Question class"""

    description: str
    choices: list[str] | None = None
    default: str | Callable[[dict[str, str]], str] | None = None

    def get_default(
        self, func: Callable[[dict[str, str]], str]
    ) -> Callable[[dict[str, str]], str]:
        """A decoractor to set the default function.

        Args:
            func: A function that takes the previous answers as the first argument and
                returns the default value.
        """
        self.default = func
        return func

    def ask(self, answers: dict[str, str], default: str | None = None) -> str:
        """Prompt user for the answer.

        Args:
            answers: The answers that have been given before.
        """
        if default is None:
            if callable(self.default):
                default = self.default(answers)
            else:
                default = self.default
        return Prompt.ask(
            self.description, console=console, choices=self.choices, default=default
        )


package_questions = {
    "name": Question("package name"),
    "version": Question("version", default="0.0.0"),
    "description": Question("description", default=""),
    "license_expr": Question("license(SPDX identifier)", default="MIT"),
    "author": Question("author"),
    "author_email": Question("author email"),
    "homepage": Question("homepage"),
    "requires_python": Question("requires_python", default=">=3.7"),
    "build_backend": Question(
        "Build backend",
        choices=["setuptools", "pdm", "flit", "hatch"],
        default="setuptools",
    ),
}


def ask_for(questions: dict[str, Question], **kwargs: str) -> dict[str, str]:
    """Ask questions and return answers.

    Args:
        questions: The questions to ask.
        **kwargs: The answers that have been given before.
    """
    answers = {}
    for key, question in questions.items():
        answers[key] = question.ask(answers, kwargs.get(key))
    return answers
