from pydantic import BaseModel, Field, ConfigDict
from typing import List


class ProcessRequest(BaseModel):
    count: int = Field(
        ...,
        ge=1,
        le=20,
        description="Number of pokemon to process (1-20)",
        examples=[5]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 5
            }
        }
    )


class PokemonData(BaseModel):
    name: str = Field(..., description="Pokemon name")
    types: List[str] = Field(default_factory=list, description="Pokemon types")
    abilities: List[str] = Field(default_factory=list, description="Pokemon abilities")
    id: int = Field(..., description="Pokemon ID")
    height: int = Field(..., description="Pokemon height")
    weight: int = Field(..., description="Pokemon weight")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "pikachu",
                "types": ["electric"],
                "abilities": ["static", "lightning-rod"],
                "id": 25,
                "height": 4,
                "weight": 60
            }
        }
    )


class ProcessResponse(BaseModel):
    item: str = Field(..., description="Pokemon name")
    result: str = Field(..., description="AI-generated description")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "item": "pikachu",
                "result": "Pikachu is a strong electric pokemon. "
                          "It possesses static, lightning-rod which make "
                          "it unique in battle. Type advantage: electric."
            }
        }
    )


class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "service": "Pokemon AI Processor",
                "version": "1.0.0"
            }
        }
    )


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Count must be between 1 and 20"
            }
        }
    )
