import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .schema import ClarifyOutput, StoryOutput

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY missing in .env")

os.environ["OPENAI_API_KEY"] = OPENROUTER_KEY
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

CLARIFY_MODEL = os.getenv("CLARIFY_MODEL", "meta-llama/llama-3.1-8b-instruct")
STORY_MODEL   = os.getenv("STORY_MODEL", "meta-llama/llama-3.1-8b-instruct")


def _load_prompt(filename: str) -> str:
    prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "agent", "prompts")
    path = os.path.join(prompt_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _call_llm(model_name: str, system: str, prompt: str) -> str:
    llm = ChatOpenAI(
        model=model_name,
        temperature=0.2,
    )
    messages = [
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content


SYSTEM_PM = (
    "You are a pragmatic Product Manager. "
    "Output ONLY valid JSON. No markdown. No explanations. No prose."
)

def ask_clarifying_questions(brd_text: str, domain: str = "generic"):
    prompt = _load_prompt("clarify.txt").replace("{BRD_TEXT}", brd_text)
    
    if domain and domain != "generic":
        domain_hint = f"\nDomain context: This is a {domain} domain project. Adjust questions to focus on {domain}-specific concerns."
        prompt += domain_hint

    raw = _call_llm(CLARIFY_MODEL, SYSTEM_PM, prompt).strip()
    print(f"[CLARIFY] Raw response (attempt 1):\n{raw}")

    try:
        data = json.loads(raw)
        ClarifyOutput.model_validate(data)
        return data
    except Exception as e:
        print(f"[CLARIFY] First attempt failed: {e}. Retrying with stricter prompt.")
        retry_prompt = prompt + "\n\nOutput ONLY valid JSON. No markdown. No text before or after JSON. Start with {."
        raw2 = _call_llm(CLARIFY_MODEL, SYSTEM_PM, retry_prompt).strip()
        print(f"[CLARIFY] Raw response (attempt 2):\n{raw2}")
        try:
            data = json.loads(raw2)
            ClarifyOutput.model_validate(data)
            return data
        except Exception as retry_err:
            print(f"[CLARIFY] Validation failed: {retry_err}")
            raise RuntimeError(f"Failed to parse clarifying questions after 2 attempts:\n{retry_err}")


def generate_user_stories(brd_text: str, answers_json: Dict[str, Any], domain: str = "generic"):
    prompt = _load_prompt("stories.txt")
    prompt = (
        prompt.replace("{BRD_TEXT}", brd_text)
        .replace("{ANSWERS_JSON}", json.dumps(answers_json, ensure_ascii=False))
    )
    
    if domain and domain != "generic":
        domain_hint = f"\nDomain context: This is a {domain} domain project. Ensure stories align with {domain} best practices."
        prompt += domain_hint

    raw = _call_llm(STORY_MODEL, SYSTEM_PM, prompt).strip()
    print(f"[STORIES] Raw response (attempt 1):\n{raw[:500]}..." if len(raw) > 500 else f"[STORIES] Raw response (attempt 1):\n{raw}")

    try:
        data = json.loads(raw)
        StoryOutput.model_validate(data)
        return data
    except Exception as e:
        print(f"[STORIES] First attempt failed: {e}. Retrying with stricter prompt.")
        retry_prompt = prompt + "\n\nOutput ONLY valid JSON. No markdown. No text before or after JSON. Start with {."
        raw2 = _call_llm(STORY_MODEL, SYSTEM_PM, retry_prompt).strip()
        print(f"[STORIES] Raw response (attempt 2):\n{raw2[:500]}..." if len(raw2) > 500 else f"[STORIES] Raw response (attempt 2):\n{raw2}")
        try:
            data = json.loads(raw2)
            StoryOutput.model_validate(data)
            return data
        except Exception as retry_err:
            print(f"[STORIES] Validation failed: {retry_err}")
            raise RuntimeError(f"Failed to parse user stories after 2 attempts:\n{retry_err}")


def style_check_stories(stories_data: Dict[str, Any]) -> Dict[str, Any]:
    issues = []
    
    for epic in stories_data.get("epics", []):
        for story in epic.get("stories", []):
            story_id = story.get("id", "unknown")
            
            acs = story.get("acceptance_criteria", [])
            if not acs:
                issues.append(f"{story_id}: Missing acceptance criteria")
            else:
                has_gherkin = any("Given" in ac or "When" in ac or "Then" in ac for ac in acs)
                if not has_gherkin:
                    issues.append(f"{story_id}: No Gherkin-style AC (missing Given/When/Then)")
            
            i_want = story.get("i_want", "").strip()
            if not i_want or len(i_want.split(",")) > 2:
                issues.append(f"{story_id}: Goal unclear or too broad (i_want)")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "stories": stories_data
    }

