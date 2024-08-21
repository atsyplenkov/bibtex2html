from g4f.client import Client
from g4f.Provider import RetryProvider, PerplexityAi, Vercel, You


# Function to send a prompt to GPT-3.5 Turbo and return the response
def ask_gpt(prompt: str) -> str:
    """
    This function sends a prompt to GPT-3.5 Turbo and returns the response.

    Args:
        prompt (str): The prompt to be sent to GPT-3.5 Turbo.

    Returns:
        str: The plain text response from GPT-3.5 Turbo.
    """
    # Try various providers
    # https://github.com/xtekky/gpt4free/blob/main/docs/client.md#use-a-list-of-providers-with-retryprovider
    client = Client(provider=RetryProvider([PerplexityAi, Vercel, You], shuffle=True))

    # Read the GPT prompt
    with open("templates/prompt.md", "r") as file:
        md_content = file.read()

    # Format the prompt by adding the content of the prompt.md file to it.
    formatted_prompt = f"{md_content}: {prompt} \n\n Make sure that only the plain text is returned, do not try to return this as a markdown code block."

    # Send the formatted prompt to GPT-3.5 Turbo and get the response.
    response = client.chat.completions.create(
        model="",
        messages=[
            {"role": "user", "content": formatted_prompt}
        ],  # The user message to be sent to the model.
    )

    # Fix the doi link
    response = response.choices[0].message.content.replace(
        "doi={https://doi.org/", "doi={"
    )

    # Return the response after stripping any leading or trailing whitespaces.
    return response.strip()


# Run ask_gpt in a for loop
def batch_ask_gpt(prompts: str) -> str:
    """
    Takes a string of newline-separated prompts and sends them to GPT-3.5 Turbo in batches of 3.

    Args:
        prompts (str): A string of newline-separated prompts.

    Returns:
        str: The concatenated plain text response from GPT-3.5 Turbo.
    """
    # Split the string into a list
    prompt_list = prompts.splitlines()

    # Split the list into chunks of 3
    prompt_list = [prompt_list[i : i + 3] for i in range(0, len(prompt_list), 3)]

    # Run gpt task
    responses = []
    for chunk in prompt_list:
        chunk_str = "\n".join(chunk)
        response = ask_gpt(chunk_str)
        responses.append(response)

    # Join the responses
    responses = "\n\n".join(responses)

    return responses

