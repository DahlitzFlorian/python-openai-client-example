from openai import OpenAI

client = OpenAI(
    api_key="<API_KEY>",
    base_url="http://<IP_ADDRESS>:8080",
    default_headers={
        "Content-Type": "application/json",
    },
)

message = input("Message: ")
if not message:
    message = "Say this is a test"


stream = client.chat.completions.create(
    messages=[{"role": "user", "content": message}],
    model="",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
