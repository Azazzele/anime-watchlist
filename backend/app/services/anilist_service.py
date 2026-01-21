import httpx
import certifi
import json
import logging

logger = logging.getLogger(__name__)

ANILIST_API_URL = "https://graphql.anilist.co"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "JukeyAnime/1.0",
}


async def anilist_query(query: str, variables: dict | None = None) -> dict:
    variables = variables or {}

    payload = {
        "query": query,
        "variables": variables,
    }

    logger.debug("AniList request")
    logger.debug(json.dumps(payload, ensure_ascii=False, indent=2))

    try:
        async with httpx.AsyncClient(
            headers=HEADERS,
            timeout=httpx.Timeout(20.0),
            verify=certifi.where(),
        ) as client:
            resp = await client.post(ANILIST_API_URL, json=payload)

        # ❗ HTTP-ошибки — реальные ошибки
        if resp.status_code != 200:
            logger.error(f"AniList HTTP {resp.status_code}: {resp.text[:300]}")
            raise RuntimeError(f"AniList HTTP error {resp.status_code}")

        result = resp.json()

        logger.debug("AniList response")
        logger.debug(json.dumps(result, ensure_ascii=False, indent=2))

        return result

    except httpx.TimeoutException:
        logger.error("AniList timeout")
        raise RuntimeError("AniList timeout")

    except httpx.RequestError as e:
        logger.error(f"AniList connection error: {e}")
        raise RuntimeError("Ошибка соединения с AniList")

    except json.JSONDecodeError:
        logger.error("AniList invalid JSON")
        raise RuntimeError("Некорректный JSON от AniList")
