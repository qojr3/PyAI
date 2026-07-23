import requests
import re


CEREBRAS_KEY = ""  # Replace with your Cerebras API key

URL = "https://api.cerebras.ai/v1/chat/completions"

MODEL = "gemma-4-31b"


def create_svg(filename, description):

    prompt = f"""
Create an SVG image.

Requirements:
- Output ONLY SVG code.
- No markdown.
- No explanation.

Description:
{description}
"""


    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {CEREBRAS_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )


    data = response.json()


    if "choices" not in data:
        print(data)
        return


    svg = data["choices"][0]["message"]["content"]


    # remove markdown fences if AI adds them
    svg = re.sub(
        r"```svg|```",
        "",
        svg
    ).strip()


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(svg)


    print(
        f"Saved SVG: {filename}"
    )