# Elden Ring Dataset API

A FastAPI-based REST API that provides access to Elden Ring game data through CSV files. This API includes JWT authentication, pagination, search functionality, and is designed for integration with data pipelines like Microsoft Fabric Data Factory.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 📊 **CSV Data Access** - Read and query CSV files containing Elden Ring data
- 🔍 **Search Functionality** - Full-text search across all data fields
- 📄 **Pagination** - Efficient data retrieval with page-based pagination
- 🗂️ **File Discovery** - List available CSV files automatically
- 🐳 **Docker Support** - Containerized deployment ready
- 🔒 **Security** - Path traversal protection and input validation
- 📈 **Data Pipeline Ready** - Optimized for integration with data pipelines

## Dataset

The API serves Elden Ring game data sourced from the ["Ultimate Elden Ring with Shadow of The Erdtree DLC" dataset](https://www.kaggle.com/datasets/pedroaltobelli/ultimate-elden-ring-with-shadow-of-the-erdtree-dlc) available on Kaggle. This comprehensive dataset was created by Pedro Altobelli using information from the [Elden Ring Wiki (Fextralife)](https://eldenring.wiki.fextralife.com/Elden+Ring+Wiki) and includes data from both the base game and the Shadow of the Erdtree DLC expansion.

**Dataset Details:**
- **Source**: Kaggle - Pedro Altobelli
- **Data Origin**: Elden Ring Wiki (Fextralife)
- **Coverage**: Base game + Shadow of the Erdtree DLC
- **License**: CC0 (Public Domain)
- **Total Size**: ~30MB across 28 files
- **DLC Identification**: Each record includes a "dlc" column (1 = DLC content, 0 = base game)

The dataset includes:

### Main Categories
- **Armors** - All armor pieces and their stats
- **Weapons** - Weapons and their upgrade paths
- **Bosses** - Boss information and statistics
- **Creatures** - Enemy creatures and their data
- **Incantations** - Faith-based spells and abilities
- **Sorceries** - Intelligence-based spells
- **Locations** - Game world locations
- **NPCs** - Non-player characters
- **Shields** - Shield data and upgrades
- **Skills** - Weapon skills and abilities
- **Spirit Ashes** - Summon data
- **Talismans** - Equipment accessories

### Items Subcategory
- **Ammos** - Ammunition types
- **Bells** - Bell items
- **Consumables** - Consumable items
- **Cookbooks** - Recipe books
- **Crystal Tears** - Flask of Wondrous Physick ingredients
- **Great Runes** - Major boss runes
- **Key Items** - Quest and progression items
- **Materials** - Crafting materials
- **Remembrances** - Boss remembrances
- **Tools** - Utility items
- **Upgrade Materials** - Weapon/armor enhancement items
- **Whetblades** - Affinity modification items

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd eldenring-api
   ```

2. **Start the API:**
   ```bash
   docker-compose up -d
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

### Local Development

1. **Prerequisites:**
   ```bash
   python 3.8+
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export DATA_DIR=./data
   export SECRET_KEY=your-secret-key-here
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Documentation

### Authentication

#### Get Access Token
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=password123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_at": "2025-11-19T17:45:00"
}
```

### Endpoints

#### 1. Root Endpoint
```http
GET /
```
Returns welcome message.

#### 2. List Available Files
```http
GET /files
Authorization: Bearer <your-token>
```

**Response:**
```json
[
  "armors.csv",
  "bosses.csv",
  "weapons.csv",
  "items/consumables.csv",
  "items/materials.csv"
]
```

#### 3. Get Data from CSV File
```http
GET /data?file=armors.csv&page=1&page_size=100&q=knight
Authorization: Bearer <your-token>
```

**Parameters:**
- `file` (required) - CSV file path (e.g., "armors.csv" or "items/consumables.csv")
- `page` (optional) - Page number (default: 1)
- `page_size` (optional) - Records per page (default: 100, max recommended: 1000)
- `q` (optional) - Search query (searches all fields)

**Response:**
```json
{
  "file": "armors.csv",
  "total_rows": 1250,
  "page": 1,
  "page_size": 100,
  "total_pages": 13,
  "rows": [
    {
      "Name": "Knight Armor",
      "Physical": "85",
      "Magic": "76",
      "Fire": "80",
      "Lightning": "77",
      "Holy": "81"
    }
  ]
}
```

## Integration Examples

### Python Client Example

```python
import requests

# Get token
auth_response = requests.post(
    "http://localhost:8000/token",
    data={"username": "admin", "password": "password123"}
)
token = auth_response.json()["access_token"]

# Set headers
headers = {"Authorization": f"Bearer {token}"}

# Get available files
files_response = requests.get("http://localhost:8000/files", headers=headers)
files = files_response.json()

# Get data with pagination
for file in files:
    page = 1
    while True:
        response = requests.get(
            f"http://localhost:8000/data",
            params={"file": file, "page": page, "page_size": 1000},
            headers=headers
        )
        data = response.json()
        
        if not data["rows"]:
            break
            
        # Process data
        print(f"Processing {len(data['rows'])} rows from {file}")
        
        page += 1
```

### PowerShell Example

```powershell
# Get token
$authBody = "username=admin&password=password123"
$tokenResponse = Invoke-RestMethod -Uri "http://localhost:8000/token" -Method Post -Body $authBody -ContentType "application/x-www-form-urlencoded"
$token = $tokenResponse.access_token

# Set headers
$headers = @{ "Authorization" = "Bearer $token" }

# Get files
$files = Invoke-RestMethod -Uri "http://localhost:8000/files" -Headers $headers

# Get data
foreach ($file in $files) {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/data?file=$file&page=1&page_size=1000" -Headers $headers
    Write-Host "File: $file, Total Rows: $($response.total_rows)"
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATA_DIR` | `./data` | Directory containing CSV files |
| `SECRET_KEY` | `CHANGE_THIS_SECRET` | JWT secret key (change in production!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiration time |

### Docker Environment

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATA_DIR=/data
      - SECRET_KEY=your-production-secret-key
    volumes:
      - ./data:/data:ro
```

## Security Notes

🔒 **Important Security Considerations:**

1. **Change the SECRET_KEY** in production environments
2. **Use HTTPS** in production
3. **Implement rate limiting** for production use
4. **Secure your data directory** with appropriate file permissions
5. **Use environment variables** for sensitive configuration
6. **Consider implementing user management** beyond hardcoded credentials

## Performance Tips

- **Optimal page_size**: Use 500-1000 for best performance with data pipelines
- **Search queries**: Use specific terms for faster search results
- **Caching**: Consider implementing Redis caching for frequently accessed data
- **File size**: Most CSV files are optimally sized for single-page requests

## Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check if token is included in Authorization header
   - Verify token hasn't expired (60 minutes default)

2. **404 File Not Found**
   - Check if file exists using `/files` endpoint
   - Verify file path format (use forward slashes)

3. **Large Response Issues**
   - Reduce `page_size` parameter to 500 or less
   - Use pagination to retrieve data in smaller chunks

4. **Docker Permission Issues**
   - Ensure data directory has proper read permissions
   - Check volume mount paths in docker-compose.yml

### Logs and Monitoring

View application logs:
```bash
docker-compose logs -f api
```

## Development

### Project Structure
```
eldenring-api/
├── app/
│   └── main.py          # FastAPI application
├── data/                # CSV data files
│   ├── armors.csv
│   ├── weapons.csv
│   └── items/
│       ├── consumables.csv
│       └── materials.csv
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Adding New Data

1. Place CSV files in the `data/` directory
2. API automatically discovers new files
3. Files are available immediately via `/files` and `/data` endpoints

## License

This project is provided as-is for educational and data analysis purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

---

**Built with FastAPI** 🚀 | **Docker Ready** 🐳 | **Data Pipeline Optimized** 📊