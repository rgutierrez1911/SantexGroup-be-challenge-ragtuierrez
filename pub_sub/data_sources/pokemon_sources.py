from typing import List
from pydantic import BaseModel
from data_sources.constants import POKEAPI_URL
import requests

class PokemonDataResult(BaseModel):
    name: str = None
    url: str = None
class PokemonResults(BaseModel):

    count: int = None
    next: str = None
    previous: str = None
    results: List[PokemonDataResult]
class PokeApiDataSource(BaseModel):
    
    url: str = POKEAPI_URL
    
    def get_paged(
        self,
        offset: int = 20,
        limit: int = 20
    ) -> dict:
        params = {
            "offset": offset,
            "limit": limit
        }
        resp = requests.get(url=self.url, params=params)

        if 200 <= resp.status_code < 300:
            return resp.json()
    
    def get_names(self, offset : int = 20 , limit : int = 20) -> List[PokemonDataResult]:
        pokemon_data = self.get_paged(offset=offset, limit=limit)

        pokemon_results = PokemonResults(**pokemon_data)

        poke_names = [result for result in pokemon_results.results]
        return poke_names
