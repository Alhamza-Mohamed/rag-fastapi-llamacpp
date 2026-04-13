# llama.cpp Setup Guide

> Running a local LLM on Windows — step by step

---

## Overview

This guide walks you through setting up llama.cpp on Windows from scratch, including installing all required tools, building the project, and running a local LLM model.

You need two things:
- **The engine** — llama.cpp (compiled from source)
- **The model weights** — a `.gguf` file

Both must be present for the server to run.

---

## What You Need

| Component | Purpose | Where to get it |
|---|---|---|
| Git | Clone llama.cpp source | https://git-scm.com |
| CMake | Build system generator | https://cmake.org/download |
| VS Build Tools | C++ compiler (MSVC) | https://visualstudio.microsoft.com/visual-cpp-build-tools |
| llama.cpp source | The inference engine | https://github.com/ggerganov/llama.cpp |
| .gguf model file | The model weights | https://huggingface.co |

---

## Step 1 — Install CMake

Download the Windows x64 installer from https://cmake.org/download and run it.

> ⚠️ During installation, select: **"Add CMake to the system PATH for all users"**

Verify the installation:

```
# PowerShell — no admin
cmake --version
```

---

## Step 2 — Install Visual Studio C++ Build Tools

Download from https://visualstudio.microsoft.com/visual-cpp-build-tools and run the installer.

Select the **"Desktop development with C++"** workload and make sure these are checked:

- MSVC v143 (or latest) build tools
- Windows 10/11 SDK
- C++ CMake tools for Windows

After installation, **restart your PC**.

---

## Step 3 — Clone llama.cpp

```
# PowerShell — no admin
cd "C:\AI\models"
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
```

---

## Step 4 — Build llama.cpp

> ⚠️ You **must** use the **x64 Native Tools Command Prompt for VS** (search for it in the Start menu).
> Regular CMD or PowerShell will NOT work for building — they don't have the MSVC compiler in their PATH.

> ⚠️ Use `cd /d` to switch drives in CMD, not just `cd`.

```
# x64 Native Tools Command Prompt — no admin
cd /d "C:\AI\models\llama.cpp"
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

This takes **10–15 minutes**. Many warnings will appear — that is normal. Wait for it to finish completely.

---

## Step 5 — Add Your Model (.gguf file)

Download a `.gguf` model from HuggingFace and place it inside your llama.cpp folder:

```
C:\AI\models\llama.cpp\
    your-model.gguf          <-- place it here
    build\
        bin\
            Release\
                llama-server.exe
```

---

## Step 6 — Run the Server

```
# CMD — no admin
cd /d "C:\AI\models\llama.cpp\build\bin\Release"
llama-server.exe -m "C:\AI\models\llama.cpp\your-model.gguf" -c 4096 --port 8080
```

Then open your browser at **http://localhost:8080** to access the chat UI.

---

## Step 7 — Create a run.bat (Optional but Recommended)

Create a file called `run.bat` in your llama.cpp folder so you can double-click it to start the server anytime:

```bat
@echo off
"C:\AI\models\llama.cpp\build\bin\Release\llama-server.exe" ^
  -m "C:\AI\models\llama.cpp\your-model.gguf" ^
  -c 4096 --port 8080
pause
```

---

## Troubleshooting

**Problem:** `cmake` not recognized  
**Solution:** CMake not installed or not added to PATH. Reinstall and check the PATH option.

**Problem:** `cl` not recognized in PowerShell  
**Solution:** Normal — `cl.exe` only works inside the x64 Native Tools Command Prompt.

**Problem:** CMake cannot find Visual Studio  
**Solution:** MSVC Build Tools not installed. Run VS Installer and add the C++ workload.

**Problem:** `cd` command doesn't change drive  
**Solution:** Use `cd /d "D:\path"` — the `/d` flag is required to switch drives in CMD.

**Problem:** CMakeCache.txt conflict error  
**Solution:** Delete the `build` folder completely and recreate it before running `cmake` again.

**Problem:** No CMakeLists.txt found  
**Solution:** You're in the wrong directory. Must be inside the llama.cpp source root, not a parent folder.

**Problem:** Server starts but model won't load  
**Solution:** Check the `.gguf` file path is correct and the file is not corrupted.

---

> **Note:** This build is CPU-only. For GPU acceleration, rebuild with CUDA toolkit installed using:
> ```
> cmake .. -DGGML_CUDA=ON
> ```
