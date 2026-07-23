# PyAI

PyAI is a terminal AI assistant powered by Cerebras.  
It can chat, remember conversations, and create SVG images.

## Features

- 💬 AI chat
- 🧠 Conversation memory
- 🎨 SVG image generation
- 📁 Custom workspace support
- ⚡ Fast terminal interface

## ⚠️ Warning

PyAI uses an AI API and can create files on your computer.

Only run code or open files that you trust.

Keep your API key private and never upload it to GitHub.

## Setup

### 1. Clone the repository

Open Git Bash and run:

```bash
git clone https://github.com/qojr3/PyAI
```

### 2. Enter the project folder

```bash
cd PyAI
```

### 3. Install requirements

```bash
pip install requests rich
```

### 4. Run PyAI

```bash
python PyAI.py
```

## Commands

| Command | Description |
|---|---|
| `/svg filename.svg description` | Creates an SVG image in `workspace/images/` |
| `/workspace folder` | Changes the workspace folder |
| `/where` | Shows the current workspace |
| `/save` | Saves chat memory to JSON |
| `/clear` | Clears chat memory |
| `/exit` | Closes PyAI |

## License

MIT License
