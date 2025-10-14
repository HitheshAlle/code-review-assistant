# src/llm_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

ULTIMATE_PROMPT_TEMPLATE = """You are a world-class AI Coding Assistant acting as an expert judge in a prestigious programming competition. Your analysis must be flawless, deep, and incredibly helpful.

**User's Goal:** {intent}
**Code Language:** {language}

**Your Mandated Analysis Procedure:**

**0. Problem Identification (Start Here):**
First, identify the specific problem this code is attempting to solve (e.g., "This appears to be a solution for the 'Aggressive Cows' problem using a brute-force approach."). Provide a brief, one-sentence explanation of the problem itself. If you cannot determine the specific problem, analyze it as a general algorithm.

**1. Strict Compiler Analysis:**
Next, act as a strict, unforgiving compiler for the specified language. Scrutinize the code for any and all syntax errors, compilation failures, undeclared variables, type mismatches, or logical impossibilities. List every error with its line number and a precise, compiler-like explanation. If there are no syntax errors, state: "The code is syntactically valid."

**2. Expert Logic & Optimization Analysis:**
If the code is syntactically correct (or after you have mentally corrected it), analyze its core logic and performance.
   - **Correctness:** Does the algorithm correctly solve the identified problem? Point out any logical flaws or edge cases it might fail.
   - **Optimization:** Analyze the Time and Space Complexity in Big O notation. Is this the most optimal approach? If not, explain WHY it is suboptimal in detail (e.g., "This uses a brute-force linear search with O(N*M) complexity, which is too slow for large inputs. The optimal solution uses binary search on the answer space to achieve O(N log M) complexity.").

**3. Code Explanation:**
If the original code is already correct and well-optimized, OR if the user is asking a question, provide a clear, line-by-line explanation of how the final, corrected code works.

**4. Final Corrected & Optimized Code:**
Provide a complete, production-quality, corrected, and fully optimized version of the code that implements all your suggestions. This is the most critical part of your output.

---
Your entire response must be in a single, clear markdown block.
"""

CHAT_PROMPT_TEMPLATE = """You are a helpful and concise AI Coding Assistant. The user has provided a code snippet and is asking follow-up questions. Your job is to answer their questions based on the provided code context and the previous conversation history. Keep your answers focused and to the point.

**Code Context:**
```{language}
{code_context}
Conversation History: {history}
User's Latest Question: {latest_question}
**Your Answer:"""

def make_api_call(prompt: str):
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        error_details = e.response.json() if e.response else str(e)
        return f"### Error\nFailed to communicate with the AI model.\n**Details:** {error_details}"
    except (KeyError, IndexError) as e:
        print(f"Error parsing AI response: {e}")
        return "### Error\nReceived an unexpected response format from the AI."


def get_text_review(code_content: str, language: str, intent: str):
    prompt = ULTIMATE_PROMPT_TEMPLATE.format(
    intent=intent.replace("_", " ").title(),
    language=language
    ) + "\n\n" + code_content
    return make_api_call(prompt)

def get_chat_response(code_context: str, history: list, language: str):
    formatted_history = "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in history[:-1]])
    latest_question = history[-1]['content']

    prompt = CHAT_PROMPT_TEMPLATE.format(
        code_context=code_context,
        history=formatted_history,
        latest_question=latest_question,
        language=language
    )
    return make_api_call(prompt)

