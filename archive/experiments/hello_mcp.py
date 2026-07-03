# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP

server = FastMCP("weather")

@server.tool()
def get_weather(city: str) -> str:
    return f"The weather in {city} is Sunny"

# Test the tool directly
print(get_weather("Dhaka"))
