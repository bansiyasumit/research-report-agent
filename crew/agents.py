"""
Agent definitions for the research/report crew.

Each agent needs: role, goal, backstory, an LLM, and (for two of them) tools.
Filled in Step 4 of the build.

Planned agents:
- research_agent      : uses the Serper search tool, gathers raw findings
- analysis_agent      : turns raw findings into structured insight
- fact_check_agent    : re-searches to independently verify the analysis
- report_writer_agent : (Phase 2) writes the final structured report
"""

from crewai import Agent


def build_research_agent(llm, search_tool) -> Agent:
    return Agent(
        role="Research Analyst",
        goal=(
            "Use live web search to gather comprehensive, current, and "
            "properly sourced information on the given topic."
        ),
        backstory=(
            "You are a meticulous research analyst who never relies on "
            "memory alone. For every claim you make, you search the web "
            "first and cite where the information came from. You favor "
            "recent, authoritative sources and note the publication or "
            "site for each fact you gather."
        ),
        llm=llm,
        tools=[search_tool],
        verbose=True,
    )


def build_analysis_agent(llm) -> Agent:
    return Agent(
        role="Insight Analyst",
        goal=(
            "Turn raw research findings into structured, well-organized "
            "insight: key themes, trends, comparisons, and implications."
        ),
        backstory=(
            "You are a sharp analyst who takes a pile of raw research "
            "notes and turns them into a coherent picture. You group "
            "related facts, surface patterns and contradictions, and "
            "highlight what actually matters for someone trying to "
            "understand the topic quickly."
        ),
        llm=llm,
        verbose=True,
    )


def build_fact_check_agent(llm, search_tool) -> Agent:
    return Agent(
        role="Fact Checker",
        goal=(
            "Independently verify the analyst's claims by re-searching "
            "the web, and explicitly flag anything that can't be "
            "confirmed or that conflicting sources dispute."
        ),
        backstory=(
            "You are a skeptical fact-checker. You do not take the "
            "analysis at face value — for every significant claim, you "
            "run your own independent search to confirm it. You call out "
            "unverifiable claims, outdated information, and disagreement "
            "between sources instead of rubber-stamping the analysis."
        ),
        llm=llm,
        tools=[search_tool],
        verbose=True,
    )


def build_report_writer_agent(llm) -> Agent:
    return Agent(
        role="Report Writer",
        goal=(
            "Turn approved, fact-checked findings into a polished, "
            "long-form structured report suitable for a business or "
            "research audience."
        ),
        backstory=(
            "You are a professional report writer who produces "
            "publication-quality documents. You never pad with filler — "
            "every section is substantive, well-organized, and backed by "
            "the findings you were given. You write in clear prose with "
            "proper Markdown structure (headings, bullet points, tables "
            "where useful) so the report reads like a real deliverable, "
            "not a chat answer."
        ),
        llm=llm,
        verbose=True,
    )
