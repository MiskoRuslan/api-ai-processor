from sentence_transformers import SentenceTransformer
from typing import List
import logging
from schemas import PokemonData, ProcessResponse

logger = logging.getLogger(__name__)


class AIProcessor:
    """AI processor for generating pokemon descriptions"""

    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("AI model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading AI model: {e}")
            self.model = None

    def process_pokemon(self, pokemon_data: PokemonData) -> str:
        if not self.model:
            return "AI model not available"

        try:
            name = pokemon_data.name
            types = pokemon_data.types
            abilities = pokemon_data.abilities

            types_str = ", ".join(types) if types else "unknown type"
            abilities_str = ", ".join(abilities[:3]) if abilities else "no abilities"

            description = self._generate_description(name, types_str, abilities_str)

            return description

        except Exception as e:
            logger.error(f"Error processing pokemon {pokemon_data.name}: {e}")
            return f"Error processing {pokemon_data.name}"

    def _generate_description(self, name: str, types: str, abilities: str) -> str:

        input_text = f"{name} is a {types} type pokemon with abilities: {abilities}"

        try:
            embedding = self.model.encode(input_text)
            magnitude = float(sum(abs(x) for x in embedding))

            if "fire" in types.lower():
                category = "powerful fire"
            elif "water" in types.lower():
                category = "aquatic"
            elif "grass" in types.lower():
                category = "nature-based"
            elif "electric" in types.lower():
                category = "electric"
            elif "psychic" in types.lower():
                category = "mystical"
            elif "dragon" in types.lower():
                category = "legendary dragon"
            else:
                category = types.split(",")[0] if "," in types else types

            strength = "strong" if magnitude > 15 else "balanced"

            description = (
                f"{name.capitalize()} is a {strength} {category} pokemon. "
                f"It possesses {abilities} which make it unique in battle. "
                f"Type advantage: {types}."
            )

            return description

        except Exception as e:
            logger.error(f"Error in description generation: {e}")
            return f"{name.capitalize()} is a {types} type pokemon with {abilities}."

    def process_multiple(self, pokemon_list: List[PokemonData]) -> List[ProcessResponse]:
        results = []

        for pokemon in pokemon_list:
            description = self.process_pokemon(pokemon)

            result = ProcessResponse(
                item=pokemon.name,
                result=description
            )
            results.append(result)

        return results
