import httpx
from fastapi import HTTPException
import certifi


ANILIST_API_URL = "https://graphql.anilist.co"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "JukeyAnime/1.0",
}

async def anilist_query(query: str, variables: dict = None):
    async with httpx.AsyncClient(headers=HEADERS, timeout=20.0,  verify=certifi.where()) as client:
        resp = await client.post(
            ANILIST_API_URL,
            json={
                "query": query,
                "variables": variables or {}
            }
        )

        resp.raise_for_status()
        return resp.json()["data"]
