"""
Task descriptions and expected_output for each agent.

The exact wording here matters a lot — it's what pushes the report
writer toward an actual 12+ page structured document instead of three
paragraphs, and what pushes the fact-checker to actually challenge
claims instead of rubber-stamping them.
Filled in Step 5 of the build.
"""

from crewai import Task


def research_task(agent, topic: str) -> Task:
    return Task(
        description=(
            f"Research the topic: '{topic}'.\n\n"
            "Use live web search to gather current, factual information. "
            "Cover, at minimum:\n"
            "- What the topic is and why it matters right now\n"
            "- Key players, companies, products, or people involved\n"
            "- Relevant statistics, figures, or market data\n"
            "- Recent news, developments, or trends (favor the last 12 "
            "months where relevant)\n"
            "- Any notable risks, controversies, or open questions\n\n"
            "Run multiple distinct searches to cover different angles of "
            "the topic rather than a single generic query. For every "
            "finding, note the source (site name or URL) it came from."
        ),
        expected_output=(
            "A detailed set of raw research notes, organized under clear "
            "subheadings, with every fact attributed to a source. This is "
            "raw material for analysis, not a polished report — "
            "completeness and sourcing matter more than prose style."
        ),
        agent=agent,
    )


def analysis_task(agent, context: list) -> Task:
    return Task(
        description=(
            "Analyze the raw research notes you were given as context. "
            "Identify the key themes, trends, and patterns. Group related "
            "facts together, compare and contrast competing players or "
            "viewpoints where relevant, and call out what the findings "
            "actually imply for someone trying to understand or act on "
            "this topic. Do not simply repeat the research notes — add "
            "structure and interpretation."
        ),
        expected_output=(
            "A structured analysis organized under clear subheadings "
            "(e.g. Key Themes, Trends, Comparisons, Implications), "
            "written in clear prose with supporting facts kept intact "
            "from the research so they can still be verified."
        ),
        agent=agent,
        context=context,
    )


def fact_check_task(agent, context: list) -> Task:
    return Task(
        description=(
            "Independently fact-check the analysis you were given as "
            "context. Do not simply restate or agree with it. For every "
            "significant claim or statistic, run your OWN web search to "
            "confirm it against a source — do not rely on the research "
            "agent's original sourcing alone. Explicitly flag:\n"
            "- Any claim you could NOT verify with your own search\n"
            "- Any claim that conflicting sources disagree on\n"
            "- Any claim that appears outdated or superseded by newer "
            "information\n\n"
            "Then produce a final, corrected set of findings that merges "
            "the verified analysis with your fact-check notes."
        ),
        expected_output=(
            "A final findings document with two parts: (1) the "
            "verified, corrected analysis ready for report writing, and "
            "(2) a clearly labeled 'Fact-Check Notes' section listing "
            "anything unverifiable, disputed, or outdated, with "
            "explanation. This combined document is what a human "
            "reviewer will read and edit before approving."
        ),
        agent=agent,
        context=context,
    )


def report_task(agent, approved_findings: str, topic: str) -> Task:
    return Task(
        description=(
            f"Using ONLY the human-approved findings below, write a full "
            f"structured, long-form report on '{topic}'. Do not invent "
            "new facts beyond what's in the approved findings — your job "
            "is to organize, expand on, and professionally present this "
            "material, not to re-research it.\n\n"
            "The report MUST be long and substantive — target roughly "
            "12+ pages worth of content (at minimum ~3000 words) — and "
            "MUST include, in this order:\n"
            "1. Title\n"
            "2. Executive Summary\n"
            "3. Market / Competitive Overview\n"
            "4. Detailed Findings (broken into multiple thematic "
            "subsections with headings, not one big block)\n"
            "5. Risks & Open Questions\n"
            "6. Recommendations\n"
            "7. Sources\n\n"
            "Write in clean Markdown with proper heading levels, bullet "
            "points and/or tables where they aid clarity. Avoid vague "
            "filler sentences — every paragraph should carry real "
            "content drawn from the approved findings.\n\n"
            "--- APPROVED FINDINGS (human-reviewed) ---\n"
            f"{approved_findings}\n"
            "--- END APPROVED FINDINGS ---"
        ),
        expected_output=(
            "A complete, long-form Markdown report following the exact "
            "section structure above, professional in tone, detailed "
            "enough to read as a real deliverable rather than a summary."
        ),
        agent=agent,
    )
