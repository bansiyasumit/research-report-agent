"""
Wraps CrewAI's SerperDevTool so the Serper API key comes from the user
at request time instead of an environment variable. This app is
multi-user, so nothing about credentials can be hardcoded or global.
Filled in Step 3 of the build.
"""

import os

from crewai_tools import SerperDevTool


def build_search_tool(serper_api_key: str) -> SerperDevTool:
    if not serper_api_key:
        raise ValueError("A Serper API key is required")

    # SerperDevTool has no constructor param for the key — crewai-tools
    # hardcodes os.environ["SERPER_API_KEY"] at request time inside the
    # tool's _run(). This is the one place this app touches os.environ,
    # and it's still driven entirely by the key the user typed into the
    # Streamlit password field this call — never hardcoded, never written
    # to a .env file, never logged.
    os.environ["SERPER_API_KEY"] = serper_api_key
    return SerperDevTool()
