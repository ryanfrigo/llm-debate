# main.py
"""
Main script for the Python Multi-Agent LLM Debate Workflow.
"""
import sys
from config import (
    OPENROUTER_API_KEY,
    PERSPECTIVE_GENERATION_MODEL,
    DEBATE_AGENT_MODEL,
    NUM_PERSPECTIVES_TO_GENERATE,
    NUM_DEBATE_ROUNDS,
)
from llm_utils import initialize_client, get_llm_response
from agents import DebateAgent, generate_perspectives

def run_debate(initial_query, agents, num_rounds):
    """
    Orchestrates the debate among agents and prints the transcript.
    """
    debate_transcript = []  # List of {"speaker": agent_name, "argument": text}
    print("\n--- DEBATE START ---")
    print(f"Topic: {initial_query}\n")
    for round_num in range(1, num_rounds + 1):
        print(f"Round {round_num}:")
        for agent in agents:
            argument = agent.argue(initial_query, debate_transcript)
            print(f"{agent.name}: {argument}\n")
            debate_transcript.append({"speaker": agent.name, "argument": argument})
    print("--- DEBATE END ---\n")
    return debate_transcript

def summarize_debate(transcript: list, client, model: str, debate_topic: str):
    """
    Uses an LLM to summarize the debate, highlighting key points.
    """
    print("\n--- DEBATE SUMMARY ---")
    
    if not transcript:
        print("No debate to summarize.")
        return

    transcript_string = "\n".join([
        f"{entry['speaker']}: {entry['argument']}" for entry in transcript
    ])

    prompt = (
        f"The following is a transcript of a debate on the topic: '{debate_topic}'.\\n\\n"
        f"Transcript:\\n{transcript_string}\\n\\n"
        "Please analyze this debate and provide a summary that includes:\\n"
        "1. The main ideas proposed by the participants.\\n"
        "2. Key points of agreement reached, if any.\\n"
        "3. Key points of disagreement or unresolved tensions. Focus on the core conflicts.\\n"
        "4. Any novel solutions, creative ideas, or synthesis that emerged from the discussion.\\n\\n"
        "Present this as a structured summary."
    )
    
    messages = [
        {"role": "system", "content": "You are an expert debate analyst. Your task is to summarize the key outcomes of a debate."},
        {"role": "user", "content": prompt}
    ]
    
    summary = get_llm_response(client, model, messages)
    print(summary)
    print("\n--- END OF SUMMARY ---")

def main():
    print("Welcome to the Multi-Agent LLM Debate!")
    api_key = input("Enter your OpenRouter API Key (or leave blank to use config.py): ").strip() or OPENROUTER_API_KEY
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY":
        print("[Error] Please provide a valid OpenRouter API Key in config.py or at the prompt.")
        sys.exit(1)
    client = initialize_client(api_key=api_key)
    user_query = input("Enter your query: ").strip()
    if not user_query:
        print("[Error] Query cannot be empty.")
        sys.exit(1)
    print("\nGenerating perspectives...")
    perspectives = generate_perspectives(
        client,
        PERSPECTIVE_GENERATION_MODEL,
        user_query,
        NUM_PERSPECTIVES_TO_GENERATE,
    )
    if not perspectives:
        print("[Error] Failed to generate perspectives. Using default perspectives.")
        perspectives = [f"Expert{i+1}" for i in range(NUM_PERSPECTIVES_TO_GENERATE)]
    print(f"Identified Perspectives: {', '.join(perspectives)}\n")
    agents = [
        DebateAgent(name=persp, client=client, model=DEBATE_AGENT_MODEL)
        for persp in perspectives
    ]
    transcript = run_debate(user_query, agents, NUM_DEBATE_ROUNDS)
    # Optionally, print the full transcript again in a structured way
    print("Full Debate Transcript:")
    for i, entry in enumerate(transcript, 1):
        print(f"{i}. {entry['speaker']}: {entry['argument']}")

    # Add summarization step
    if transcript: #Only summarize if there's a transcript
        summarize_debate(transcript, client, DEBATE_AGENT_MODEL, user_query)

if __name__ == "__main__":
    main() 