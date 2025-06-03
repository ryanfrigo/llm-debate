# agents.py
"""
Defines the DebateAgent class and the perspective generation function.
"""
from typing import List, Dict
from llm_utils import get_llm_response

class DebateAgent:
    def __init__(self, name: str, client, model: str, system_prompt_template: str = None):
        self.name = name
        self.client = client
        self.model = model
        self.system_prompt_template = system_prompt_template or (
            "You are {perspective_name}, a sharp and critical thinker. The debate topic is: '{topic}'.\n"
            "The discussion so far:\n{history_string}\n\n"
            "**Your primary task is to directly challenge, refine, or build upon the last 1-2 points made, especially the immediately preceding one. **"
            "Be specific in your critique: identify flaws, risks, or unsupported assumptions. Ask clarifying or challenging questions. "
            "Adopt an assertive but constructive and professional tone. Do not be overly agreeable. Clearly identify areas of disagreement. "
            "After addressing the previous points, you may introduce new arguments or insights relevant to your perspective. "
            "What is your incisive contribution?"
        )

    def argue(self, debate_topic: str, debate_history: List[Dict[str, str]]) -> str:
        history_string = "(No arguments yet.)"
        last_speaker = "N/A"
        last_argument = "N/A"

        if debate_history:
            history_entries = []
            for i, entry in enumerate(debate_history):
                history_entries.append(f"Turn {i+1} - {entry['speaker']}: {entry['argument']}")
            history_string = "\n".join(history_entries)
            
            # Get the last speaker and their argument for focused rebuttal
            last_entry = debate_history[-1]
            last_speaker = last_entry['speaker']
            last_argument = last_entry['argument']

        # System prompt remains generic about the role, user prompt carries specific instructions.
        system_role_prompt = f"You are an AI assistant embodying the role of {self.name}, a highly critical and analytical expert in your field."
        
        # Construct a focused user prompt
        if not debate_history:
            user_prompt_content = self.system_prompt_template.format(
                perspective_name=self.name,
                topic=debate_topic,
                history_string=history_string 
            )
        else:
            # Tailor prompt to focus on the last speaker
            user_prompt_content = (
                f"You are {self.name}, a sharp and critical thinker. The debate topic is: '{debate_topic}'.\n"
                f"The discussion so far:\n{history_string}\n\n"
                f"The last speaker, {last_speaker}, argued: '{last_argument}'\n\n"
                f"**Your primary goal now is to critically analyze {last_speaker}'s statement. Challenge it, identify flaws, ask probing questions, or build upon it with significant modifications. Be specific and assertive.** "
                f"After thoroughly addressing {last_speaker}'s point, you may add other new points relevant to your role. "
                f"What is your incisive contribution, {self.name}?"
            )

        messages = [
            {"role": "system", "content": system_role_prompt},
            {"role": "user", "content": user_prompt_content}
        ]
        return get_llm_response(self.client, self.model, messages)

def generate_perspectives(client, model: str, user_query: str, num_perspectives: int) -> List[str]:
    """
    Uses the LLM to generate a list of expert perspectives for the debate,
    aiming for perspectives that are likely to have differing viewpoints.
    """
    prompt = (
        f"Given the user's query: '{user_query}', I need to generate {num_perspectives} distinct and potentially contrasting expert perspectives "
        f"that would lead to a dynamic and critical debate to find the best answer. These perspectives should naturally encourage disagreement and robust discussion. "
        "For example, if the query is about a new technology, consider perspectives like 'Tech Optimist', 'Tech Skeptic', 'Ethicist', 'Regulator', 'Investor', 'End-User Advocate'. "
        "Return only a comma-separated list of these {num_perspectives} perspective names, e.g., Perspective1, Perspective2, Perspective3."
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant for brainstorming expert perspectives."},
        {"role": "user", "content": prompt}
    ]
    response = get_llm_response(client, model, messages)
    # Parse the response into a list
    if not response or "error" in response.lower():
        return []
    # Split by comma, strip whitespace
    perspectives = [p.strip() for p in response.split(",") if p.strip()]
    return perspectives 