import openai
api_key = "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"

try:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("OpenAI API Error:", e)
