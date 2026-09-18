"""
Assembles the two crews that make the human-in-the-loop checkpoint work
in a web app. CrewAI's built-in Task(human_input=True) blocks on a
terminal input() call, which doesn't exist inside Streamlit — so instead
this app splits the work into two separate crews and pauses BETWEEN them.

Phase 1 crew: research_agent -> analysis_agent -> fact_check_agent
  (sequential). Runs automatically. Its combined output is shown to the
  user in an editable box for review — that box IS the checkpoint.

Phase 2 crew: report_writer_agent
  Runs only after the user clicks approve. The approved/edited text is
  passed in as the task's context, not re-derived by the agents.

Filled in Step 6 of the build.
"""

from crewai import Crew, Process

from crew.agents import (
    build_analysis_agent,
    build_fact_check_agent,
    build_report_writer_agent,
    build_research_agent,
)
from crew.tasks import analysis_task, fact_check_task, report_task, research_task


def build_phase1_crew(llm, search_tool, topic: str) -> Crew:
    research_agent = build_research_agent(llm, search_tool)
    analysis_agent = build_analysis_agent(llm)
    fact_check_agent = build_fact_check_agent(llm, search_tool)

    t1 = research_task(research_agent, topic)
    t2 = analysis_task(analysis_agent, context=[t1])
    t3 = fact_check_task(fact_check_agent, context=[t2])

    return Crew(
        agents=[research_agent, analysis_agent, fact_check_agent],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
    )


def build_phase2_crew(llm, approved_findings: str, topic: str) -> Crew:
    report_writer_agent = build_report_writer_agent(llm)

    # approved_findings is the human-edited text from the Streamlit
    # checkpoint, baked directly into the task description below — the
    # report writer works from that, not from a re-run of Phase 1.
    t = report_task(report_writer_agent, approved_findings, topic)

    return Crew(
        agents=[report_writer_agent],
        tasks=[t],
        process=Process.sequential,
        verbose=True,
    )
