

# 📋 PROJECT SPECIFICATION: Study Notes Agent (Existing UV Project)

**ROLE:** You are a Senior Python AI Engineer.
**PRIMARY RESOURCE:** You have access to **Context7**, which holds the documentation for the `openai-agents` Python library.
**ENVIRONMENT:** The user has **already initialized** a `uv` project. You are working inside an active project root.

## 📜 THE CONSTITUTION (Rules of Construction)
1.  **Source of Truth:** Query **Context7** to understand the `openai-agents` syntax.
2.  **Strict Constraint:** **DO NOT** import or use the standard `openai` client library (e.g., `import openai`). You must rely entirely on the `openai-agents` SDK wrapper.
3.  **Dependency Management:** Use `uv add` to install packages into the existing environment.
4.  **MVP Architecture:** Single Agent instance. Simple input/output flow.

---

## 📅 IMPLEMENTATION PLAN

### PHASE 1: PREPARE STRUCTURE & DEPENDENCIES
**Instruction to CLI:**
1.  **Dependencies:** Provide the exact command to add the necessary libraries to the existing project:
    *   Command: `uv add openai-agents streamlit pypdf python-dotenv`
2.  **Structure:** Provide the shell commands (Linux/Mac style) to create the necessary files:
    *   `touch .env`
    *   `touch app.py`
    *   `mkdir utils`
    *   `touch utils/pdf_handler.py`
    *   `mkdir agent`
    *   `touch agent/logic.py`
3.  **Config:** Generate the content for `.env` (Template: `OPENAI_API_KEY=sk-...`).

### PHASE 2: THE DATA TOOL (`utils/pdf_handler.py`)
**Instruction to CLI:**
Write the content for `utils/pdf_handler.py`:
1.  Import `pypdf`.
2.  Define `extract_text(pdf_file)`.
3.  **Logic:** Accept a file object (from Streamlit), extract text from all pages, clean whitespace, and return the string.
4.  **Error Handling:** Use a `try/except` block to return a clean error message if the PDF is corrupt.

### PHASE 3: THE AGENT BACKEND (`agent/logic.py`)
**Instruction to CLI:**
**CRITICAL STEP:** Use your tools to search Context7 for: *"How to initialize an Agent in openai-agents without importing the raw openai client"*.

Based on that documentation, write `agent/logic.py`:
1.  **Imports:** Import `os`, `dotenv`, and the `Agent` class **directly from `openai-agents`**.
2.  **Config:** Load the `OPENAI_API_KEY` using `load_dotenv()`.
3.  **Class Definition:** Create a `StudyAssistant` class.
    *   *Initialize:* Instantiate the Agent using the SDK's syntax.
    *   *Function:* Define `process_task(task_instruction, pdf_content)`.
    *   *Logic:*
        1.  Construct a prompt: `f"DOCUMENT:\n{pdf_content}\n\nTASK:\n{task_instruction}"`.
        2.  Call the Agent's execution method (check Context7 if it is `.run()`, `.chat()`, or `.completion()`).
        3.  Return the text response.

### PHASE 4: THE USER INTERFACE (`app.py`)
**Instruction to CLI:**
Write the content for `app.py`:
1.  **Imports:** `streamlit`, `utils.pdf_handler`, and `agent.logic`.
2.  **Session State:** Use `st.session_state` to store the extracted PDF text.
3.  **Layout:**
    *   **Sidebar:** File Uploader ("Upload Lecture PDF").
        *   *On Change:* Run `extract_text` and update session state.
    *   **Main Area:**
        *   **Tab 1 (Summarizer):** Button "Generate Notes". Calls `StudyAssistant` with: *"Summarize this text into key concepts."*
        *   **Tab 2 (Quizzer):** Button "Generate Quiz". Calls `StudyAssistant` with: *"Create 5 MCQs based on this text."*
4.  **Display:** Render output using `st.markdown()`.

---

**🚀 EXECUTION COMMAND:**
"Gemini, please acknowledge this plan. Start by querying Context7 to learn the **pure** `openai-agents` import syntax. Then, provide the **`uv add` command** and the **file creation commands** for Phase 1."
