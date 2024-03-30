from llama_index import PromptTemplate


personality = ""
task = ""

context_str = """\
    Your Personality is: {personality}
    What you are asked to do: {task}
"""

instruction_str = """
1.
"""

query_str = ""

pandas_prompt = PromptTemplate(
    """\
    {context_str}
    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Expression: 
    """
)
