# desC

**desC** is a cross-platform desktop AI assistant for **macOS**, **Windows**, and **Linux**.

It combines a clean LLM chat interface with a project-aware assistant for **code repositories** and **document folders** using advanced contextual RAG.

desC is designed for users who want a local desktop AI workspace that can chat with LLM servers, inspect projects, index folders, understand codebases, summarize documents, and assist with project-aware generation or editing tasks.

---

## Overview

**desC** focuses on three main workflows:

1. **General LLM chat**
   - Connect to your preferred LLM provider or local server.
   - Chat in a clean desktop interface.
   - Retry, clear, and manage long conversations easily.

2. **Project-aware code assistance**
   - Select a project directory.
   - Index the project.
   - Ask questions about your codebase.
   - Request edits, explanations, rewrites, or generation tasks.

3. **Document folder assistance**
   - Use the same project-aware workflow for document folders.
   - Summarize, explain, or query documents using contextual retrieval.

desC uses a contextual RAG workflow to provide better answers based on files inside your selected project or document folder.

---

## Screenshots

### Chat

![Chat screenshot](preview/desC.png)

### Chat Server Settings

![Chat server settings](preview/desC-setting.png)

### Pinned Window

![Pinned window](preview/desC-pinned.png)

### Code Settings

![Code settings](preview/desC-Code-setting.png)

### Project-Aware HTML Generation

![Generating HTML from a project](preview/desC-Code-generating.png)

---

## Features

| Feature | Description |
| --- | --- |
| **LLM chat** | Chat with your configured LLM server or provider |
| **Project-aware assistant** | Ask questions about code repositories or document folders |
| **Advanced contextual RAG** | Retrieve relevant project context for better answers |
| **Project indexing** | Index selected folders before asking project-specific questions |
| **Ask mode** | Ask questions about code, documents, or project structure |
| **Edit mode** | Request rewrites, improvements, refactors, or content changes |
| **Apply mode** | Run or apply project-aware tasks with terminal-style interaction |
| **Clipboard preview** | Detect copied text and attach it to the next message |
| **Pinned window** | Keep desC always on top in a compact assistant window |
| **Chat minimap** | Navigate long conversations more easily |
| **Retry message** | Restore and retry the last user message |
| **Dark/light themes** | Use desC comfortably in either theme |
| **Cross-platform** | Available for macOS, Windows, and Linux |

---

## Supported Platforms

desC is available for:

- **macOS**
- **Windows**
- **Linux**

Download the correct binary for your operating system from the latest release.

---

## Requirements

desC requires:

```text
Python 3.13 only
```

> The binary is built for **Python 3.13**, so all required Python packages must be installed using **Python 3.13**.

This is important because dependencies installed with another Python version may not work with desC.

---

## Download

Download desC from the latest GitHub release:

```text
https://github.com/mambo06/MMP/tree/main/Client
```

Choose the binary for your platform:

- macOS
- Windows
- Linux

---

## Installation

### 1. Download desC

Download the latest release for your operating system.

### 2. Move desC to a writable folder

Place desC in a folder where the app has permission to create files, install dependencies, store runtime data, and download the embedding model.

Good examples:

#### Windows

```text
C:\desC
D:\Apps\desC
```

#### macOS

```text
~/Desktop/desC
~/Applications/desC
```

#### Linux

```text
/home/your-user/desC
~/desC
```

### 3. Avoid protected folders

Do **not** run desC from protected folders such as:

```text
Documents
Program Files
System folders
Read-only locations
Restricted enterprise folders
```

desC needs write access for:

- Python dependency installation
- Runtime files
- Project indexing data
- Embedding model download
- Configuration storage

### 4. Run the app

Start desC.

On first launch, desC may ask to install Python dependencies.

Make sure dependencies are installed with:

```text
Python 3.13
```

### 5. Restart desC

After dependencies are installed, close and reopen the app.

### 6. Wait for model download

On startup, desC downloads a Hugging Face embedding model used for contextual RAG.

Approximate download size:

```text
100 MB
```

The first launch may take longer while this model is downloaded.

---

## First-Time Setup

desC has two main areas:

- **Chat**
- **Code**

The Code tab uses the LLM server configured in the Chat tab, so configure Chat first.

---

## Chat Setup

Before using Chat:

1. Open the **Chat** tab.
2. Open the server/provider settings.
3. Select your provider.
4. Use the default local desC or enter your LLM server details.
5. Enter your model name if required.
6. Enter your API key if required.
7. Save the settings.
8. Start chatting.

The current provider is shown in the header area of the Chat tab.

---

## Code and Document Project Setup

Before using project-aware assistance:

1. Set up your LLM provider in the **Chat** tab.
2. Open the **Code** tab.
3. Open **Code Settings**.
4. Select your project directory.
5. Save and validate the settings.
6. Click **Index project**.
7. Ask questions about your code or documents.

The selected folder can be:

- A code repository
- A documentation folder
- A mixed project containing source files and documents

---

## Using desC

### Chat Tab

The **Chat** tab provides a standard LLM chat interface.

You can use it to:

- Ask general questions
- Brainstorm ideas
- Generate text
- Debug snippets
- Interact with local or remote LLM providers

Chat features include:

- Provider selector
- Retry last message
- Clear conversation
- Clipboard preview
- Always-on-top pinned window
- Chat minimap for long conversations
- Dark and light theme support


---

### Code Tab

The **Code** tab provides project-aware assistance.

You can use it to:

- Explain a project structure
- Ask questions about files
- Generate code based on the project
- Summarize documents
- Request edits or rewrites
- Apply project-aware tasks
- Interact with terminal-style prompts in Apply mode

Before using the Code tab effectively, you should:

1. Configure a project path.
2. Save and validate.
3. Index the project.

---

## Project Indexing

Project indexing allows desC to understand the contents of your selected folder.

To index a project:

1. Open the **Code** tab.
2. Open the action menu.
3. Click **Index project**.
4. Wait for indexing to complete.

Indexing is required before asking project-specific questions.


## Documents / Code (Project) Assistant Modes

The Code assistant supports three modes:

| Mode | Purpose |
| --- | --- |
| **Ask** | Ask questions about code or documents |
| **Edit** | Request rewrites, improvements, refactors, or content changes |
| **Apply** | Apply or execute project-aware tasks |

### Ask Mode

Use **Ask** mode when you want explanations or analysis.

Examples:

```text
Explain the architecture of this project.
```

```text
What does the ChatScreen class do?
```

```text
Summarize the documents in this folder.
```

### Edit Mode

Use **Edit** mode when you want suggested changes, rewrites, or improvements.

Examples:

```text
Improve the README based on the current project.
```

```text
Refactor the chat screen for better readability.
```

```text
Rewrite this document in a more professional tone.
```

### Apply Mode

Use **Apply** mode for project-aware actions that may require step-by-step execution or user confirmation.

Examples:

```text
Generate a new HTML page for this project.
```

```text
Create documentation based on the indexed source files.
```

```text
Apply the suggested changes to the selected project.
```

When desC is waiting for input during an Apply task, the input bar can be used to answer terminal-style prompts.

---

## Clipboard Preview and Attachments

desC monitors copied text and can attach it to your next message.

When copied text is detected, desC shows a preview panel:

```text
Copied text detected (will be attached to message)
```

You can:

- Send it with your next message
- Add your own text before sending
- Dismiss it using the close button

If you type a message while clipboard preview is active, desC sends both:

```text
Your message

Copied clipboard text
```

This is useful for:

- Asking questions about copied code
- Explaining copied errors
- Summarizing copied text
- Sending copied logs to the assistant

---

## Pinned Window Mode

desC supports an always-on-top pinned mode.

When enabled, the window:

- Stays above other windows
- Resizes into a compact assistant panel
- Centers on the screen
- Hides the minimap to save space

This is useful while:

- Coding in another editor
- Reading documentation
- Debugging
- Copying and asking about snippets
- Keeping the assistant visible during work

You can toggle pinned mode from the header using the pin button.

---

## Chat Minimap

For long conversations, desC provides a minimap.

The minimap helps you:

- Navigate long chats
- See conversation structure
- Jump through message-heavy sessions more easily

The minimap is hidden automatically in pinned mode to preserve space.

---

## Supported LLM Providers

desC supports configuration for:

- **desC default server**
- **Local server**
- **Ollama**
- **Groq**
- **Google Gemini**
- **OpenAI-compatible endpoints**

Provider setup can include:

- Server address
- Port
- Model name
- API key

The Code tab uses the LLM server configured in the Chat tab.

---

## Example Prompts

### General Chat

```text
Explain the difference between RAG and fine-tuning.
```

```text
Help me write a product description for this app.
```

```text
Summarize this copied text.
```

### Code Project Questions

```text
Explain this project structure.
```

```text
Which file controls the chat interface?
```

```text
How does clipboard monitoring work in this app?
```

```text
Where is the pinned window behavior implemented?
```

### Document Folder Questions

```text
Summarize the documents in this folder.
```

```text
Find the main requirements mentioned in these documents.
```

```text
Create a concise overview from the indexed files.
```

### Generation Tasks

```text
Generate an HTML page based on this project.
```

```text
Create a GitHub README for this repository.
```

```text
Write user documentation for the app.
```

### Refactoring and Editing

```text
Suggest improvements for the ChatScreen UI.
```

```text
Rewrite this documentation to be clearer.
```

```text
Refactor this code for readability.
```

---

## Recommended Folder Locations

Use a writable folder for desC.

### Recommended

```text
C:\desC
D:\Apps\desC
~/Desktop/desC
~/Applications/desC
/home/your-user/desC
```

### Avoid

```text
Documents
Program Files
System folders
Protected folders
Read-only folders
Cloud folders with restricted permissions
```

---

## Important Notes

- desC must be run from a writable folder.
- Do not run it from protected folders such as `Documents`.
- Python dependencies must be installed with **Python 3.13**.
- The Code tab uses the LLM server configured in the Chat tab.
- You should index your project before asking project-specific questions.
- The embedding model is downloaded on startup and is approximately **100 MB**.
- Both code repositories and document folders can be used as projects.
- If project-aware answers seem incomplete, re-index the project.

---

## Troubleshooting

### desC cannot install dependencies

Make sure:

- Python 3.13 is installed.
- desC is in a writable folder.
- The app has permission to create files.
- You are not running it from a protected system directory.

### Code tab does not answer project-specific questions

Try the following:

1. Open the Chat tab.
2. Confirm your LLM server settings are valid.
3. Open the Code tab.
4. Open Code Settings.
5. Confirm the project path is correct.
6. Save and validate.
7. Click **Index project**.
8. Ask again.

### Model download is slow

The embedding model is approximately:

```text
100 MB
```

The LLM model is approximately:

```text
1.2 GB uses qwen-3.5
```
The first launch may take longer depending on your internet connection.

Total RAM usage approximately:

```text
2 GB
```

### Provider connection fails

Check:

- Server address
- Port
- Model name
- API key
- Local server status
- Provider compatibility
- Internet connection for hosted providers

### Pinned window does not resize correctly

Try toggling pinned mode off and on again.

If the issue continues:

1. Close desC.
2. Reopen desC.
3. Try pinned mode again.

### Clipboard preview appears unexpectedly

desC detects copied text automatically.

You can dismiss the clipboard preview using the close button on the preview panel.

---

## FAQ

### Does desC work offline?

desC works locally on your device or with local providers such as a local server or Ollama, but initial setup may require internet access to download dependencies and the embedding model.

### Does desC include an LLM?

desC connects to LLM providers or servers. You configure the provider in the Chat tab.

### Can I use desC with Ollama?

Yes. desC supports Ollama provider configuration.

### Can I use desC with OpenAI-compatible APIs?

Yes. desC supports OpenAI-compatible endpoints.

### Can desC inspect my codebase?

Yes. Select your project folder in Code Settings, save and validate, then index the project.

### Can desC summarize documents?

Yes. You can select a document folder as your project path and index it.

### Why do I need Python 3.13?

The desC binary is built for **Python 3.13**, so dependencies must be installed with the same Python version.

### Why should I avoid the Documents folder?

Some systems protect or restrict the Documents folder. desC needs write access to install dependencies, store runtime files, and download models.

### Does the Code tab use separate provider settings?

No. The Code tab uses the LLM server configured in the Chat tab.

---

## Development Notes

The UI is built with Flutter and includes:

- A main chat screen with tab navigation
- A Chat tab for provider-based LLM interaction
- A Code tab for project-aware assistance
- Clipboard monitoring support
- Window pinning support
- Scroll minimap support
- Provider and project configuration dialogues

---

## Security and Privacy

desC works with the provider or server you configure.

Depending on your setup, prompts and project context may be sent to:

- A local server
- Ollama
- Groq
- Google Gemini
- An OpenAI-compatible endpoint
- Another configured provider

Review your provider settings and privacy requirements before indexing or sending sensitive code or documents.

For private projects, consider using the desC provided or a local LLM server.

---

## Best Practices

For best results:

- Configure the Chat provider before using the Code tab.
- Use a clean project root when indexing.
- Re-index after major project changes.
- Use Ask mode for explanations.
- Use Edit mode for rewrites or improvements.
- Use Apply mode for task execution.
- Keep desC in a writable folder.
- Use Python 3.13 for all dependencies.

---

## License

```text
MIT License
```

---
