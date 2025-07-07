
import os
from elasticsearch import Elasticsearch
from fastmcp import FastMCP

# Configuration from environment variables
ES_URL = os.getenv("ES_URL", "http://localhost:9200")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

# Initialize Elasticsearch client
if ES_API_KEY:
    es = Elasticsearch([ES_URL], api_key=ES_API_KEY)
elif ES_USERNAME and ES_PASSWORD:
    es = Elasticsearch([ES_URL], http_auth=(ES_USERNAME, ES_PASSWORD))
else:
    # No authentication
    es = Elasticsearch([ES_URL])

# Instantiate FastMCP server
mcp = FastMCP("Elasticsearch MCP Server")

@mcp.tool
def list_indices() -> list[str]:
    """Return all index names."""
    try:
        return list(es.indices.get_alias().keys())
    except Exception as e:
        return {"error": str(e)}

@mcp.tool
def get_mappings(index: str) -> dict:
    """Return index mappings."""
    try:
        return es.indices.get_mapping(index=index)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool
def search(index: str, query: dict) -> dict:
    """Execute a search query."""
    print(f"Received query: {query}")
    try:
        return es.search(index=index, body=query)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
