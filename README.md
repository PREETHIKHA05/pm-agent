# Product Manager Agent (BRD → Questions → User Stories)

Convert Business Requirements into structured user stories using an LLM.

## Setup

1. **Create virtual environment and install dependencies**:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure .env**:
```
OPENROUTER_API_KEY=sk-or-...your-key...
CLARIFY_MODEL=meta-llama/llama-3.1-8b-instruct
STORY_MODEL=meta-llama/llama-3.1-8b-instruct
```

3. **Run the app**:
```powershell
streamlit run app/main.py
```

Visit `http://localhost:8501`

## Tasks

### Task B: Clarification Flow
1. Paste a BRD into the text box
2. Click "Generate 8 Clarifying Questions"
3. Verify output is JSON with exactly 8 questions
4. BRD and questions are persisted to `pm_agent.db`

**Validation**: Each question ≤ 20 words, covers required types (scope, actor, data, edge_case, security, kpi, integration, acceptance).

### Task C: Answers & Stories
1. Answer the 8 generated questions in Tab 2
2. Click "Save Answers"
3. Go to Tab 3 and click "Generate User Stories JSON"
4. Verify output includes:
   - 1–3 epics, 5–12 total stories
   - Each story: `id` (US-###), `as_a`, `i_want`, `so_that`, `acceptance_criteria[]`, `priority`
   - `nfrs` array with non-functional requirements

### Task D: Validation & Retry
- Pydantic schemas validate all JSON output
- If LLM returns invalid JSON, app retries with stricter instruction: "Output ONLY valid JSON. No extra text."
- Final output passes schema validation (no prose, no backticks)

### Task E: Samples & Outputs
Sample BRDs in `samples/`:
- `logistics_pod.txt` — Proof of delivery feature
- `fintech_kyc.txt` — KYC onboarding flow
- `healthcare_appointment.txt` — Appointment scheduling

Example outputs in `outputs/`:
- `logistics_pod_questions.json`
- `fintech_kyc_questions.json`
- `healthcare_appointment_questions.json`

## Features

- **Domain Profile Dropdown**: Select Logistics/Fintech/Healthcare to bias prompts
- **Last 5 Runs History**: View and replay previous BRD runs below the text box
- **Style Checker**: Validates stories have Gherkin-style acceptance criteria and clear goals
- **Export Formats**:
  - Markdown (`.md`) — Human-readable
  - CSV (`.csv`) — Jira-importable
  - JSON (`.json`) — Structured data

## Project Structure

```
app/
  main.py                 (Streamlit UI)
  __init__.py
  services/
    llm.py               (LLM calls, validation, style checker)
    schema.py            (Pydantic models)
    export.py            (Markdown, CSV export)
    __init__.py

agent/
  prompts/
    clarify.txt          (Question generation prompt)
    stories.txt          (Story generation prompt)

samples/
  logistics_pod.txt
  fintech_kyc.txt
  healthcare_appointment.txt

outputs/
  *_questions.json       (Example outputs)

.env                     (Your API key)
requirements.txt
pm_agent.db             (SQLite database, auto-created)
```

## Validation Checklist

- ✅ Clarifying questions: exactly 8, short (≤20 words), cover required types
- ✅ Stories: 5–12, each with clear role/goal/benefit and testable Gherkin ACs
- ✅ JSON valid against schema; unknowns marked "TBD"
- ✅ Streamlit app runs locally; outputs persist to SQLite
- ✅ README includes setup steps

## Technology Stack

- **Streamlit**: Web UI
- **LangChain**: LLM integration
- **Pydantic**: Schema validation
- **SQLite**: Persistent storage
- **OpenRouter**: API provider (compatible with OpenAI)

