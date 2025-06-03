<div align="center">

# 🗣️ llm-debate

**Multi-Agent LLM Debate CLI**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Pit multiple AI perspectives against each other to find better answers.*

</div>

---

## What is this?

A lightweight CLI tool that uses multiple LLM-powered agents to **debate any topic**. Given a query, the system:

1. **Generates perspectives** — an LLM proposes distinct expert viewpoints (e.g., "Tech Optimist", "Ethicist", "Regulator")
2. **Runs a structured debate** — each agent argues its position across multiple rounds, directly challenging previous points
3. **Summarizes the outcome** — a final LLM pass distills key agreements, disagreements, and novel insights

All powered by [OpenRouter](https://openrouter.ai) (access 100+ models with one API key).

## Quick Start

```bash
# Clone
git clone https://github.com/ryanfrigo/llm-debate.git
cd llm-debate

# Install dependency
pip install openai

# Set your API key
export OPENROUTER_API_KEY=sk-or-...

# Run
python main.py
```

You'll be prompted for a debate topic. That's it.

## Example

```
Enter your query: Should AI be open-sourced or kept proprietary?

Generating perspectives...
Identified Perspectives: Open-Source Advocate, Corporate Strategist, AI Safety Researcher

--- DEBATE START ---
Round 1:
Open-Source Advocate: ...
Corporate Strategist: ...
AI Safety Researcher: ...

Round 2: ...
--- DEBATE END ---

--- DEBATE SUMMARY ---
1. Main ideas proposed...
2. Key points of agreement...
3. Key points of disagreement...
4. Novel solutions that emerged...
--- END OF SUMMARY ---
```

## Configuration

Edit `config.py` or set environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | *required* |
| `PERSPECTIVE_GENERATION_MODEL` | Model for generating perspectives | `deepseek/deepseek-chat-v3-0324:free` |
| `DEBATE_AGENT_MODEL` | Model for agent arguments | `deepseek/deepseek-chat-v3-0324:free` |
| `NUM_PERSPECTIVES_TO_GENERATE` | Number of debaters | `3` |
| `NUM_DEBATE_ROUNDS` | Rounds of debate | `3` |

## Project Structure

```
llm-debate/
├── main.py          # Entry point & debate orchestration
├── agents.py        # DebateAgent class & perspective generation
├── llm_utils.py     # OpenRouter client utilities
├── config.py        # Configuration (env vars)
├── requirements.txt # Dependencies
└── .env.example     # Environment template
```

## How It Works

Each agent receives the full debate transcript and is prompted to **directly challenge** the previous speaker's arguments. This produces genuinely adversarial discussion rather than polite agreement — closer to how real experts debate.

The debate uses a simple but effective architecture:
- **System prompt**: Sets the agent's expert identity
- **User prompt**: Includes full transcript + explicit instructions to rebut the last speaker
- **Temperature 0.7**: Balanced between creativity and coherence

## Dependencies

Just `openai` — that's it. No frameworks, no bloat.

```bash
pip install openai
```

## License

MIT — see [LICENSE](LICENSE).
