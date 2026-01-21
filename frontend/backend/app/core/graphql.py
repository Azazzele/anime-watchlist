from pathlib import Path
from functools import lru_cache

# app/
BASE_DIR = Path(__file__).resolve().parents[1]

# app/api/v1/graphql_queries
GQL_DIR = BASE_DIR / "api" / "v1" / "graphql_queries"


@lru_cache
def gql(name: str) -> str:
    """
    Загружает GraphQL запрос из .gql файла по имени
    gql("current_season") -> current_season.gql
    """
    path = GQL_DIR / f"{name}.gql"

    if not path.exists():
        raise FileNotFoundError(f"GraphQL file not found: {path}")

    return path.read_text(encoding="utf-8")
