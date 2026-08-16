from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage


class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    origin: str
    country: str
    target_cities: list[str]
    duration_days: int
    flight_results: str
    hotel_results: str
    weather_results: str
    itinerary: str
    llm_calls: Annotated[int, operator.add]