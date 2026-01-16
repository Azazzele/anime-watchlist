import httpx
import certifi
import json


ANILIST_API_URL = "https://graphql.anilist.co"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "JukeyAnime/1.0",
}


async def anilist_query(query: str, variables: dict | None = None) -> dict:
    async with httpx.AsyncClient(
        headers=HEADERS,
        timeout=20.0,
        verify=certifi.where(),
    ) as client:
        resp = await client.post(
            ANILIST_API_URL,
            json={
                "query": query,
                "variables": variables or {},
            },
        )

        
        payload = resp.json()

        
        if "errors" in payload:
            raise RuntimeError(
                "AniList GraphQL error:\n"
                + json.dumps(payload["errors"], indent=2, ensure_ascii=False)
            )

        
        resp.raise_for_status()

        return payload["data"]
