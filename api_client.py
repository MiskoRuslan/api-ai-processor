import requests
from typing import List, Optional
import logging
import random
from schemas import PokemonData

logger = logging.getLogger(__name__)

POKEMON_API_BASE = "https://pokeapi.co/api/v2/pokemon"
MAX_POKEMON_ID = 1025
# Татал кількість покемонів в API (станом на Gen 9)
# Так, це бед практайс, просто хотілось зтягувати рандомних, а не 20 перших :)


class PokemonAPIClient:

    def __init__(self):
        self.base_url = POKEMON_API_BASE
        self.timeout = 10

    def fetch_pokemon(self, count: int) -> List[PokemonData]:
        if not 1 <= count <= 20:
            raise ValueError("Count must be between 1 and 20")

        pokemon_ids = random.sample(range(1, MAX_POKEMON_ID + 1), count)

        pokemon_list = []

        for pokemon_id in pokemon_ids:
            try:
                pokemon_data = self._fetch_single_pokemon(pokemon_id)
                if pokemon_data:
                    pokemon_list.append(pokemon_data)
            except Exception as e:
                logger.error(f"Error fetching pokemon {pokemon_id}: {e}")
                continue

        return pokemon_list

    def _fetch_single_pokemon(self, pokemon_id: int) -> Optional[PokemonData]:
        try:
            url = f"{self.base_url}/{pokemon_id}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            pokemon_data = PokemonData(
                name=data.get("name", "Unknown"),
                types=[t["type"]["name"] for t in data.get("types", [])],
                abilities=[a["ability"]["name"] for a in data.get("abilities", [])],
                id=data.get("id", 0),
                height=data.get("height", 0),
                weight=data.get("weight", 0)
            )

            return pokemon_data

        except requests.RequestException as e:
            logger.error(f"Request failed for pokemon {pokemon_id}: {e}")
            return None
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing data for pokemon {pokemon_id}: {e}")
            return None
