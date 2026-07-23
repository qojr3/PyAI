import requests
import json
import os

from rich.console import Console
from rich.markdown import Markdown


console = Console()


# =========================
# SETTINGS
# =========================

CEREBRAS_KEY = ""  # Replace with your Cerebras API key

MODEL = "gemma-4-31b"

API_URL = "https://api.cerebras.ai/v1/chat/completions"

MEMORY_FILE = "memory.json"

workspace = os.getcwd()



# =========================
# MEMORY
# =========================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return [
        {
            "role": "system",
            "content":
            "You are PyAI, a helpful AI assistant."
        }
    ]


messages = load_memory()



def save_memory():

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            messages,
            f,
            indent=4
        )



# =========================
# CHAT
# =========================

def ask_ai(prompt):

    messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    response = requests.post(

        API_URL,

        headers={
            "Authorization":
            f"Bearer {CEREBRAS_KEY}",

            "Content-Type":
            "application/json"
        },

        json={
            "model":MODEL,
            "messages":messages,
            "temperature":0.7
        }
    )


    data = response.json()


    if "choices" not in data:

        return str(data)


    answer = (
        data["choices"][0]
        ["message"]
        ["content"]
    )


    messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )


    save_memory()


    return answer



# =========================
# SVG
# =========================

def create_svg(filename, description):

    global workspace


    prompt = f"""
Create ONLY SVG code.

Rules:
- Start with <svg
- End with </svg>
- No markdown
- No explanation

Image:
{description}
"""


    response = requests.post(

        API_URL,

        headers={
            "Authorization":
            f"Bearer {CEREBRAS_KEY}",

            "Content-Type":
            "application/json"
        },

        json={
            "model":MODEL,

            "messages":[
                {
                    "role":"user",
                    "content":prompt
                }
            ],

            "temperature":0.2
        }
    )


    data = response.json()


    if "choices" not in data:

        print(data)
        return


    svg = (
        data["choices"][0]
        ["message"]
        ["content"]
    )


    svg = svg.replace(
        "```svg",
        ""
    )

    svg = svg.replace(
        "```",
        ""
    )


    start = svg.find("<svg")
    end = svg.rfind("</svg>")


    if start == -1 or end == -1:

        print(
            "Invalid SVG"
        )

        return


    svg = svg[start:end+6]


    image_folder = os.path.join(
        workspace,
        "images"
    )


    os.makedirs(
        image_folder,
        exist_ok=True
    )


    path = os.path.join(
        image_folder,
        filename
    )


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(svg)


    print(
        "Saved:",
        path
    )



# =========================
# MAIN
# =========================

console.print(
    "[cyan]PyAI Beta[/cyan]"
)


print(
"""
Commands:

/svg filename.svg description
/workspace folder
/where
/save
/clear
/exit

"""
)



while True:

    user = console.input(
        "\n[green]You:[/green] "
    )


    if user == "/exit":

        break



    elif user == "/where":

        print(
            "Workspace:",
            workspace
        )



    elif user.startswith("/workspace"):

        path = user[11:].strip()


        if os.path.exists(path):

            workspace = path

            print(
                "Workspace set:",
                workspace
            )

        else:

            print(
                "Folder does not exist"
            )



    elif user.startswith("/svg"):

        parts = user.split(
            " ",
            2
        )


        if len(parts) < 3:

            print(
                "Usage: /svg file.svg description"
            )

            continue


        create_svg(
            parts[1],
            parts[2]
        )



    elif user == "/save":

        save_memory()

        print(
            "Saved"
        )



    elif user == "/clear":

        messages = [
            {
                "role":"system",
                "content":
                "You are PyAI, a helpful AI assistant."
            }
        ]

        save_memory()

        print(
            "Cleared"
        )



    else:

        answer = ask_ai(user)

        console.print(
            Markdown(answer)
        )