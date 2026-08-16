import json
import re
from typing import Any, Dict
from schemas.travel_state import TravelState
from core.llm_gateway import acomplete


async def planner_node(state: TravelState) -> Dict[str, Any]:
    """
    Lightweight planner node that extracts travel intent and resolves
    countries/regions into concrete target cities before specialist agents run.
    """
    query = state.get("user_query", "")

    prompt = f"""You are a travel destination planner. Analyze this travel request and extract key parameters.
Request: "{query}"

Respond with ONLY a valid JSON object matching this schema:
{{
  "origin": "<departure city if mentioned, otherwise empty string>",
  "country": "<destination country or region>",
  "target_cities": ["<List of 1 to 3 specific city names. If the user only gave a country (e.g. Japan, Italy) or region, resolve to the capital and top 1-2 most popular tourist cities>"],
  "duration_days": <number of days as integer, default 5 if unspecified>
}}
"""

    try:
        response_text = await acomplete(
            prompt,
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            data = json.loads(response_text)

        target_cities = [
            c.strip()
            for c in data.get("target_cities", [])
            if isinstance(c, str) and c.strip()
        ]
        if not target_cities and query:
            target_cities = [query.strip()]

        return {
            "origin": data.get("origin", ""),
            "country": data.get("country", ""),
            "target_cities": target_cities,
            "duration_days": int(data.get("duration_days", 5)),
            "llm_calls": 1,
        }
    except Exception:
        # Fallback gracefully
        return {
            "origin": "",
            "country": "",
            "target_cities": [query.strip()] if query else [],
            "duration_days": 5,
            "llm_calls": 1,
        }
