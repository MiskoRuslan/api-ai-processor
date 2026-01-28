from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
from typing import List, Dict

from api_client import PokemonAPIClient
from ai_processor import AIProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pokemon AI Processor",
    description="API for processing Pokemon data with AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

pokemon_client = PokemonAPIClient()
ai_processor = AIProcessor()


class ProcessRequest(BaseModel):
    count: int = Field(
        ...,
        ge=1,
        le=20,
        description="Number of pokemon to process (1-20)"
    )


class ProcessResponse(BaseModel):
    """Response model for processed pokemon"""
    item: str
    result: str


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/process", response_model=List[ProcessResponse])
async def process_pokemon(request: ProcessRequest):
    try:
        logger.info(f"Processing request for {request.count} pokemon")

        pokemon_list = pokemon_client.fetch_pokemon(request.count)

        if not pokemon_list:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch pokemon data from API"
            )

        logger.info(f"Fetched {len(pokemon_list)} pokemon from API")
        results = ai_processor.process_multiple(pokemon_list)

        logger.info(f"Successfully processed {len(results)} pokemon")

        return results

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Pokemon AI Processor",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    logger.info("Starting Pokemon AI Processor service...")
    logger.info("Open http://localhost:8000 in browser")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
