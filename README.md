# Pokemon AI Processor

A FastAPI-based web service that fetches Pokemon data from the PokeAPI and generates AI-powered descriptions using sentence transformers.

## Features

- **Pokemon Data Fetching**: Retrieves Pokemon information from the public PokeAPI
- **AI Processing**: Generates natural language descriptions using sentence-transformers (all-MiniLM-L6-v2 model)
- **Modern Web Interface**: Clean, responsive frontend with real-time results
- **REST API**: Simple POST endpoint for programmatic access
- **Modular Architecture**: Clean separation of concerns with dedicated modules

## Project Structure

```
api-ai-processor/
├── main.py              # FastAPI application and server startup
├── api_client.py        # Pokemon API client
├── ai_processor.py      # AI model integration and processing
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── static/
│   ├── index.html      # Web interface
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
```

## Requirements

- Python 3.8 or higher
- Internet connection (for downloading AI model on first run and accessing PokeAPI)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: On first run, the sentence-transformers library will download the AI model (approximately 80MB). This is a one-time download.

## Usage

### Starting the Server

Run the application with a single command:

```bash
python main.py
```

The server will start on `http://localhost:8000`

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a number between 1 and 20 (number of Pokemon to process)
3. Click "Process Pokemon"
4. View the AI-generated descriptions for each Pokemon

### Using the API Directly

You can also make direct API calls:

**Endpoint**: `POST /process`

**Request**:
```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"count": 5}'
```

**Response**:
```json
[
  {
    "item": "bulbasaur",
    "result": "Bulbasaur is a balanced grass, poison pokemon. It possesses overgrow, chlorophyll which make it unique in battle. Type advantage: grass, poison."
  },
  {
    "item": "ivysaur",
    "result": "Ivysaur is a strong nature-based pokemon. It possesses overgrow, chlorophyll which make it unique in battle. Type advantage: grass, poison."
  }
  // ... more results
]
```

**Error Response** (invalid count):
```json
{
  "detail": "Count must be between 1 and 20"
}
```

### Health Check

Check if the service is running:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Pokemon AI Processor",
  "version": "1.0.0"
}
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## How It Works

1. **API Client** (`api_client.py`):
   - Fetches Pokemon data from `https://pokeapi.co/api/v2/pokemon`
   - Extracts relevant fields: name, types, abilities, height, weight

2. **AI Processor** (`ai_processor.py`):
   - Uses the `all-MiniLM-L6-v2` sentence transformer model
   - Generates embeddings from Pokemon characteristics
   - Creates natural language descriptions based on types and abilities

3. **FastAPI Server** (`main.py`):
   - Provides REST API endpoint
   - Handles request validation
   - Serves static frontend files
   - Manages error handling and logging

4. **Frontend** (`static/`):
   - Modern, responsive web interface
   - Real-time form validation
   - Loading states and error handling
   - Animated result cards

## Error Handling

The application handles various error scenarios:

- **Invalid count**: Returns 400 Bad Request if count is not between 1-20
- **API failures**: Logs errors and continues processing remaining Pokemon
- **AI processing errors**: Falls back to basic descriptions
- **Network issues**: Returns appropriate error messages to the client

## Development

### Running in Development Mode

The application runs in development mode by default with auto-reload enabled.

### Logging

The application logs important events to the console:
- Startup information
- Request processing
- Errors and warnings

### Extending the Project

The modular architecture makes it easy to extend:

- **Add new data sources**: Create a new client in a separate module
- **Use different AI models**: Modify `ai_processor.py` to use other models
- **Add more endpoints**: Add new routes in `main.py`
- **Enhance frontend**: Modify files in the `static/` directory

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Requests**: HTTP library for API calls
- **Sentence Transformers**: State-of-the-art sentence embeddings
- **PyTorch**: Deep learning framework (dependency of sentence-transformers)
- **Pydantic**: Data validation using Python type annotations

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can run on a different port:

```python
# In main.py, change the port number:
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Model Download Issues

If the AI model fails to download, ensure you have:
- Active internet connection
- Sufficient disk space (~200MB for model and dependencies)
- Proper firewall/proxy settings

### CORS Errors

The application has CORS enabled for all origins in development. For production, you should restrict allowed origins in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    # ... other settings
)
```

## License

This project is provided as-is for educational and demonstration purposes.

## Credits

- Pokemon data provided by [PokeAPI](https://pokeapi.co)
- AI model: `all-MiniLM-L6-v2` from [Sentence Transformers](https://www.sbert.net)

---

**Author**: Claude
**Version**: 1.0.0
**Date**: 2026-01-28
