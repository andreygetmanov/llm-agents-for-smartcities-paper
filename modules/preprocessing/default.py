import json

from requests import Response


def parse_answer(res):
    """
    No valid docstring found.
    """

    answer_separator = "ANSWER: "

    if answer_separator in res:
        return res.split(answer_separator)[1].strip()
    else:
        return res


def llama_70b_postprocessing(response: Response) -> str:
    """
    Extracts the relevant answer text from a model-generated response by parsing the structured output.

    Args:
        response (Response): Recieved model's response.

    Returns:
        str: Processed output containing only answer on asked question.

    """

    return parse_answer(json.loads(response.text)["content"])


def llama_8b_postprocessing(response: Response) -> str:
    """
    Extracts and processes the generated answer text from the response object returned by the language model API.

    Args:
        response (Response): Recieved model's response.

    Returns:
        str: Processed output containing only answer on asked question.

    """

    return parse_answer(json.loads(response.text)["choices"][0]["message"]["content"])


def vsegpt_postprocessing(response: Response) -> str:
    """
    Extracts and formats the relevant textual response from the provided model output.

    Args:
        response (Response): Recieved model's response.

    Returns:
        str: Processed output containing only answer on asked question.

    """

    return parse_answer(response.choices[0].message.content)
