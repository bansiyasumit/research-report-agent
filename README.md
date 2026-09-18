# Research & Report Automation Agent

A multi-agent system (CrewAI) that researches a topic using live web search,
verifies its own claims, pauses for human review, then writes a structured
report — using a free Google Gemini API key *you* supply at runtime.
No key is stored anywhere; each user brings their own.

## How it works
1. Open the app, pick a Gemini model, paste your Gemini API key and a
   Serper (web search) API key.
2. Type a research topic.
3. Phase 1 crew (Research -> Analysis -> Fact-check agents) runs automatically.
4. Review and edit the combined findings right in the app — this is the
   human-in-the-loop checkpoint.
5. Phase 2 crew (Report writer agent) turns your approved findings into a
   full structured report.
6. Download the report as PDF or DOCX.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Getting free API keys
- Gemini (Google AI Studio): https://aistudio.google.com/apikey — free, no card
- Serper (web search): https://serper.dev — 2,500 free searches

## Project layout
```
research-report-agent/
├── app.py                  Streamlit UI
├── crew/
│   ├── agents.py             The 4 agents
│   ├── tasks.py                What each agent is asked to do
│   ├── tools.py                  Serper search wrapper
│   └── crew_builder.py            Assembles Phase 1 / Phase 2 crews
├── utils/
│   ├── llm_factory.py            UI selection -> CrewAI LLM object
│   └── report_export.py            Markdown -> PDF / DOCX
└── requirements.txt
```

**Status:** fully implemented — agents, tasks, the two-phase crew,
Streamlit UI, and PDF/DOCX export are all in place.
