from fastapi import APIRouter

router = APIRouter()

@router.get("/episodes")
def search_episodes(q: str = ""):
    # OPTIONAL: search over episode cards if you expose them via API
    return {"query": q, "results": []}
