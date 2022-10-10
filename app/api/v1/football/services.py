
from commons.clients.football_client import async_client


async def competitions_by_league(league: str):
  async with async_client.aio_client.get(f"/v4/competitions/{league}") as resp:
    return await resp.json()


async def teams_by_league(league: str):
  async with async_client.aio_client.get(f"/v4/competitions/{league}/teams") as resp:
    return await resp.json()
