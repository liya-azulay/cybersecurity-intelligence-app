# API Documentation

## Overview

The Cybersecurity Intelligence API provides endpoints for managing and searching MITRE ATT&CK attack patterns. The API is built with FastAPI and provides automatic OpenAPI documentation.

## Base URL

- **Development**: `http://localhost:8000`
- **API Base**: `http://localhost:8000/api/v1`

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication mechanisms.

## Data Models

### AttackPattern

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "x_mitre_platforms": ["string"],
  "x_mitre_detection": "string",
  "phase_name": "string",
  "external_id": "string",
  "kill_chain_phases": ["string"],
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

### SearchRequest

```json
{
  "query": "string",
  "limit": "integer (optional, default: 50)",
  "offset": "integer (optional, default: 0)"
}
```

### SearchResponse

```json
{
  "results": [AttackPattern],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

## Endpoints

### Health Check

#### GET /api/v1/health

Check if the API is running.

**Response:**

```json
{
  "status": "healthy",
  "message": "Cybersecurity Intelligence API is running"
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/health
```

## Cyber Bot API

### Chat with Cyber Bot

#### POST /api/v1/bot/chat

Send a message to the cyber bot and get an intelligent response.

**Request Body:**

```json
{
  "message": "Show me all persistence techniques",
  "user_id": "user123"
}
```

**Response:**

```json
{
  "response": "I found 15 persistence techniques in the database. Here are the most common ones: T1543.003 (Create or Modify System Process: Windows Service), T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder)...",
  "suggestions": [
    "Show me more details about T1543.003",
    "What are the detection methods for persistence?",
    "Search for Windows-specific techniques"
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/bot/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all persistence techniques", "user_id": "user123"}'
```

### Get Bot Statistics

#### GET /api/v1/bot/stats

Get statistics about bot usage and performance.

**Response:**

```json
{
  "total_commands": 150,
  "successful_commands": 142,
  "failed_commands": 8,
  "most_used_commands": [
    {"command": "search", "count": 45},
    {"command": "details", "count": 32},
    {"command": "virustotal", "count": 28}
  ],
  "average_response_time": 1.2
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/bot/stats
```

### Bot Health Check

#### GET /api/v1/bot/health

Check if the bot service is running and healthy.

**Response:**

```json
{
  "status": "healthy",
  "bot_version": "1.0.0",
  "last_activity": "2024-01-15T10:30:00Z",
  "active_connections": 3
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/bot/health
```

### Get Available Commands

#### GET /api/v1/bot/commands

Get list of available bot commands and their descriptions.

**Response:**

```json
{
  "commands": [
    {
      "name": "search",
      "description": "Search for attack patterns in the database",
      "example": "search for persistence techniques"
    },
    {
      "name": "details",
      "description": "Get detailed information about a specific technique",
      "example": "show me details about T1543.003"
    },
    {
      "name": "virustotal",
      "description": "Analyze a file or hash using VirusTotal",
      "example": "analyze this hash: 1234567890abcdef"
    },
    {
      "name": "stats",
      "description": "Get statistics about attack patterns",
      "example": "show me statistics"
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/bot/commands
```

### Get All Attack Patterns

#### GET /api/v1/attack-patterns

Retrieve all attack patterns with pagination.

**Query Parameters:**

- `limit` (integer, optional): Number of results to return (default: 50, max: 100)
- `offset` (integer, optional): Number of results to skip (default: 0)

**Response:**

```json
{
  "results": [AttackPattern],
  "total": 1500,
  "limit": 50,
  "offset": 0
}
```

**Example:**

```bash
curl "http://localhost:8000/api/v1/attack-patterns?limit=10&offset=0"
```

### Search Attack Patterns

#### POST /api/v1/attack-patterns/search

Search attack patterns by description (case-insensitive).

**Request Body:**

```json
{
  "query": "DLL injection",
  "limit": 20,
  "offset": 0
}
```

**Response:**

```json
{
  "results": [AttackPattern],
  "total": 5,
  "limit": 20,
  "offset": 0
}
```

**Example:**

```bash
curl -X POST "http://localhost:8000/api/v1/attack-patterns/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "DLL injection", "limit": 10}'
```

### Get Specific Attack Pattern

#### GET /api/v1/attack-patterns/{pattern_id}

Retrieve a specific attack pattern by ID.

**Path Parameters:**

- `pattern_id` (string): The unique identifier of the attack pattern

**Response:**

```json
{
  "id": "T1001",
  "name": "Data Obfuscation",
  "description": "Adversaries may obfuscate data...",
  "x_mitre_platforms": ["Windows", "Linux"],
  "x_mitre_detection": "Monitor network traffic...",
  "phase_name": "Defense Evasion",
  "external_id": "T1001",
  "kill_chain_phases": ["defense-evasion"],
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/attack-patterns/T1001
```

### Get Statistics

#### GET /api/v1/stats

Retrieve statistics about attack patterns.

**Response:**

```json
{
  "total_patterns": 1500,
  "phase_distribution": [
    {
      "_id": "Execution",
      "count": 250
    },
    {
      "_id": "Persistence",
      "count": 200
    }
  ],
  "platform_distribution": [
    {
      "_id": "Windows",
      "count": 800
    },
    {
      "_id": "Linux",
      "count": 400
    }
  ]
}
```

**Example:**

```bash
curl http://localhost:8000/api/v1/stats
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found

```json
{
  "detail": "Attack pattern with ID T9999 not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, implement rate limiting to prevent abuse.

## CORS

The API is configured to allow requests from:

- `http://localhost:3000` (React development server)
- `http://127.0.0.1:3000` (Alternative localhost)

For production, update CORS settings to match your frontend domain.

## Data Ingestion

### Populate Database

To populate the database with MITRE ATT&CK data:

```bash
cd backend
python data_ingestion.py
```

This script will:

1. Fetch data from the MITRE ATT&CK GitHub repository
2. Process and transform the data
3. Store it in MongoDB
4. Provide a count of imported patterns

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:

- Explore all available endpoints
- Test API calls directly from the browser
- View request/response schemas
- Download OpenAPI specification

## Example Usage

### JavaScript/TypeScript

```typescript
// Get all attack patterns
const response = await fetch(
  "http://localhost:8000/api/v1/attack-patterns?limit=10",
);
const data = await response.json();

// Search attack patterns
const searchResponse = await fetch(
  "http://localhost:8000/api/v1/attack-patterns/search",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: "malware",
      limit: 20,
    }),
  },
);
const searchData = await searchResponse.json();
```

### Python

```python
import requests

# Get all attack patterns
response = requests.get('http://localhost:8000/api/v1/attack-patterns?limit=10')
data = response.json()

# Search attack patterns
search_response = requests.post(
    'http://localhost:8000/api/v1/attack-patterns/search',
    json={
        'query': 'malware',
        'limit': 20
    }
)
search_data = search_response.json()
```

### cURL

```bash
# Get attack patterns
curl "http://localhost:8000/api/v1/attack-patterns?limit=10"

# Search attack patterns
curl -X POST "http://localhost:8000/api/v1/attack-patterns/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "malware", "limit": 20}'

# Get specific pattern
curl "http://localhost:8000/api/v1/attack-patterns/T1001"

# Get statistics
curl "http://localhost:8000/api/v1/stats"

# Chat with cyber bot
curl -X POST "http://localhost:8000/api/v1/bot/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all persistence techniques", "user_id": "user123"}'

# Get bot statistics
curl "http://localhost:8000/api/v1/bot/stats"

# Get bot health
curl "http://localhost:8000/api/v1/bot/health"

# Get available commands
curl "http://localhost:8000/api/v1/bot/commands"
```

## Performance Considerations

- **Pagination**: Always use pagination for large result sets
- **Search**: Search queries are case-insensitive and use regex
- **Caching**: Consider implementing caching for frequently accessed data
- **Database Indexing**: Ensure proper indexes on search fields

## Security Considerations

- **Input Validation**: All inputs are validated using Pydantic models
- **SQL Injection**: Not applicable (MongoDB), but input sanitization is important
- **CORS**: Configure appropriately for production
- **Rate Limiting**: Implement in production
- **Authentication**: Add proper authentication for production use
