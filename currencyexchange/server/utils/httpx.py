from httpx import AsyncClient


async def get(endpoint: str, params: dict = {}, headers: dict = {}) -> dict:
    async with AsyncClient() as client:
        response = await client.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
