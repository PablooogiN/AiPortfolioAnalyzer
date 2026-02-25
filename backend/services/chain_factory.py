"""Builds a LangChain LCEL chain for a given investing strategy.

Each chain uses one-shot prompting: system prompt -> example human/AI pair ->
real user input. Returns the full response via .ainvoke().
"""

import os

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from services.examples import EXAMPLE_INPUT, EXAMPLE_OUTPUTS
from services.strategies import get_strategy_prompt


def build_chain(strategy_key: str):
    system_prompt = get_strategy_prompt(strategy_key)
    example_output = EXAMPLE_OUTPUTS.get(strategy_key, EXAMPLE_OUTPUTS["value"])

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("human", "{example_input}"),
            ("ai", "{example_output}"),
            ("human", "{user_input}"),
        ]
    )

    llm = ChatAnthropic(
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=2048,
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    # Bind the static values so callers only need to pass user_input
    bound = prompt.partial(
        system_prompt=system_prompt,
        example_input=EXAMPLE_INPUT,
        example_output=example_output,
    )

    return bound | llm
