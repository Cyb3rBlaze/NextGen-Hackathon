import openai_async

async def generate_response(prompt):
    response = await openai_async.chat_complete(
        api_key,
        timeout=20,
        payload={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    # Get the response text from the API response
    response_text = response.json()["choices"][0]["message"]['content']

    return response_text