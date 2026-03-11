from app.agent.tools import weather_tool


def test_weather_tool_returns_string():
    result = weather_tool("London")
    assert isinstance(result, str)
    assert "London" in result