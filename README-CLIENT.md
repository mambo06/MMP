# desC

**desC** is a desktop AI assistant for **macOS**, **Windows**, and **Linux**.

It combines a clean LLM chat interface with a project-aware assistant for **code** and **document** folders using advanced contextual RAG.

---

> ⚠️ **Unsigned Application Notice**
>
> desC is currently an **unsigned application**. macOS and Windows will show a security warning on first launch.
> This is expected — follow the platform-specific steps below to allow it to run.

---

> 📦 **First Launch — Model Download**
>
> On first startup, desC will automatically download the **LLM and embedding models** required for chat and RAG features.
> Please allow time for this to complete before using the app.
>
> Approximate download size: **~2 GB**
> Make sure you have a stable internet connection and enough disk space before launching.

---

## Screenshots

### Chat

![Chat screenshot](images/chat-ss.png)

### Chat Server Settings

![Chat server settings](images/chat-server-setting-ss.png)

### Pinned Window

![Pinned window](images/pinned-windows-ss.png)

### Code Settings

![Code settings](images/code-setting.png)

### Project-Aware HTML Generation

![Generating HTML from a project](images/code-sample-generating-html-from-project.png)

---

## Features

- **Chat with your LLM server**
- **Project-aware code assistant**
- **Document project support**
- **Advanced contextual RAG**
- **Project indexing**
- **Ask, Edit, and Apply modes**
- **Clipboard preview and attachment**
- **Always-on-top pinned window**
- **Chat minimap for long conversations**
- **Dark and light theme support**
- **macOS, Windows, and Linux support**

---

## Getting Started

### 1. Download desC

Download the binary for your platform from the latest release:

- macOS
- Windows
- Linux

### 2. Move it to a writable folder

Place desC somewhere the app can write files.

Good examples:

```text
C:\desC
D:\Apps\desC
~/Desktop/desC
~/Applications/desC
/home/your-user/desC
```

> Important: avoid protected folders such as `Documents`.

desC needs write access to install dependencies, store runtime files, and download the embedding model.

### 3. Run the app

Start desC by following the platform-specific steps below.

### 4. Wait for model download

On first startup, desC will automatically download the LLM and embedding models (~2 GB).
Do not close the app during this process.

---

## Running on macOS (Unsigned App)

macOS will block desC from running because it is not signed with an Apple Developer certificate.

### First-time launch

1. Locate `desC.app` in Finder.
2. **Right-click** (or Control-click) on the app.
3. Select **Open** from the context menu.
4. A dialog will appear warning that the app is from an unidentified developer.
5. Click **Open** to confirm.

> You only need to do this once. After the first launch, desC will open normally.

### If the Open option does not appear

Open **System Settings** → **Privacy & Security**, scroll down to the Security section, and click **Open Anyway** next to the desC entry.

Or run this command in Terminal to remove the quarantine flag:

```bash
xattr -cr /path/to/desC.app
```

---

## Running on Windows (Unsigned App)

Windows Defender SmartScreen will show a warning because desC is not signed with a code-signing certificate.

### First-time launch

1. Double-click `desC.exe`.
2. A blue SmartScreen dialog will appear: **"Windows protected your PC"**.
3. Click **More info**.
4. Click **Run anyway**.

> You only need to do this once per installation.

### If Windows Defender blocks the file after download

1. Right-click `desC.exe` in File Explorer.
2. Select **Properties**.
3. At the bottom of the General tab, check **Unblock**.
4. Click **Apply** → **OK**.
5. Run the app again.

---

## Running on Linux

### AppImage

```bash
chmod +x desC-x86_64.AppImage
./desC-x86_64.AppImage
```

If nothing happens, install FUSE first:

```bash
sudo apt install libfuse2
./desC-x86_64.AppImage
```

---

## First-Time Setup

### Chat

Before using Chat:

1. Open the **Chat** tab.
2. Open server/provider settings.
3. Enter your LLM server details.
4. Save.
5. Start chatting.

### Code and Documents

Before using project-aware assistance:

1. Set the LLM server in the **Chat** tab.
2. Open the **Code** tab.
3. Open **Code Settings**.
4. Select your project directory.
5. Save and validate.
6. Click **Index project**.
7. Ask questions about your code or documents.

Example prompts:

```text
Explain this project structure.
```

```text
Generate an HTML page based on this project.
```

```text
Summarize the documents in this folder.
```

---

## Code Assistant Modes

| Mode | Use |
| --- | --- |
| **Ask** | Ask questions about code or documents |
| **Edit** | Request changes, rewrites, or improvements |
| **Apply** | Apply or execute project-aware tasks |

---

## Supported Providers

desC supports server/provider setup for:

- Local server
- Ollama
- Groq
- Google Gemini
- OpenAI-compatible endpoints

---

## Notes

- Run desC from a writable folder.
- Do not run it from protected locations such as `Documents`.
- The Code tab uses the LLM server configured in the Chat tab.
- Index your project before asking project-specific questions.
- Both code repositories and document folders are supported.
