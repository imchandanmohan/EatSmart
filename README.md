# EatSmart - Smart Food Shopping Assistant

## Overview

EatSmart is a Model Context Protocol (MCP) connector that transforms your grocery shopping experience by providing intelligent food analysis and recommendations. It integrates with OpenFoodFacts API to deliver comprehensive nutritional information, product images, and personalized shopping reports directly through your preferred LLM interface.

## Features

### 🔍 **Smart Food Analysis**
- Real-time product lookup using OpenFoodFacts database
- Comprehensive nutritional information extraction
- Product image retrieval and analysis
- Ingredient breakdown and allergen detection

### 📊 **RAG-Powered Intelligence**
- Vector-based similarity search for product recommendations
- Contextual understanding of dietary preferences and restrictions
- Historical shopping pattern analysis
- Nutritional goal tracking and optimization

### 📧 **Smart Shopping Lists**
- Automated email generation with detailed product information
- Interactive checkbox format for easy shopping
- Product images included for visual identification
- Total nutrition summary and health scoring

### 📈 **Comprehensive Reports**
- Overall health score for your shopping basket
- Nutritional balance analysis
- Budget optimization suggestions
- Dietary goal alignment assessment

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LLM Client    │◄──►│  EatSmart MCP    │◄──►│  OpenFoodFacts  │
│   (Claude/GPT)  │    │   Connector      │    │      API        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Email Service   │
                       │  (SMTP/SendGrid) │
                       └──────────────────┘
```

## MCP Integration

This project implements the Model Context Protocol to provide:
- **Tools**: Product lookup, nutrition analysis, shopping list generation
- **Resources**: OpenFoodFacts database access, user preference storage
- **Prompts**: Smart shopping assistant, nutrition counselor, budget optimizer

## Technology Stack

- **Python 3.13+**
- **MCP SDK**: Model Context Protocol implementation
- **FastAPI**: RESTful API endpoints
- **OpenFoodFacts API**: Food database integration
- **Vector Database**: RAG implementation (ChromaDB/Pinecone)
- **Email Services**: SMTP/SendGrid integration
- **Image Processing**: Pillow/OpenCV for product images

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/eatsmart.git
cd eatsmart

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and SMTP settings
```

## Configuration

Create a `.env` file with the following variables:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Optional: External APIs
SENDGRID_API_KEY=your-sendgrid-key

# Vector Database (if using Pinecone)
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=your-environment

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

## Usage

### MCP Server Mode
```bash
python main.py --mode mcp-server
```

### Standalone API Mode
```bash
python main.py --mode api
```

### CLI Mode
```bash
python main.py --product "coca cola" --email user@example.com
```

## MCP Tools Available

### 1. `lookup_product`
Search for products in OpenFoodFacts database
```json
{
  "name": "lookup_product",
  "description": "Search for food products and get nutritional information",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Product name or barcode"},
      "limit": {"type": "integer", "default": 10}
    }
  }
}
```

### 2. `analyze_nutrition`
Analyze nutritional content and provide health insights
```json
{
  "name": "analyze_nutrition",
  "description": "Analyze nutritional data and provide health recommendations",
  "inputSchema": {
    "type": "object",
    "properties": {
      "products": {"type": "array", "items": {"type": "string"}},
      "dietary_goals": {"type": "string", "description": "User's dietary preferences"}
    }
  }
}
```

### 3. `generate_shopping_email`
Create comprehensive shopping list with analysis
```json
{
  "name": "generate_shopping_email",
  "description": "Generate detailed shopping email with product analysis",
  "inputSchema": {
    "type": "object",
    "properties": {
      "email": {"type": "string", "format": "email"},
      "products": {"type": "array"},
      "include_images": {"type": "boolean", "default": true}
    }
  }
}
```

## RAG Implementation

EatSmart uses Retrieval-Augmented Generation for:

1. **Product Similarity**: Vector embeddings of product descriptions
2. **Nutritional Knowledge**: Indexed nutritional guidelines and recommendations
3. **User Preferences**: Personalized recommendation based on shopping history
4. **Dietary Patterns**: Pattern recognition for health optimization

## Example Workflow

1. User asks LLM: "I want to buy healthy breakfast options for a family of 4"
2. LLM calls `lookup_product` tool with relevant queries
3. EatSmart searches OpenFoodFacts and retrieves product data
4. RAG system provides contextual nutritional recommendations
5. `analyze_nutrition` provides health scoring and insights
6. `generate_shopping_email` creates comprehensive shopping list
7. Email sent with products, images, checkboxes, and health report

## Development

### Project Structure
```
eatsmart/
├── main.py                          # Entry point (already exists)
├── README.md                        # Project documentation (already exists)
├── requirements.txt                 # Dependencies (already exists)
├── pyproject.toml                   # Project configuration (already exists)
├── LICENSE                          # Apache 2.0 License (already exists)
├── .python-version                  # Python version (already exists)
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore patterns
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Application settings
│   └── logging_config.py            # Logging configuration
├── src/
│   ├── __init__.py
│   ├── eatsmart/
│   │   ├── __init__.py
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── server.py            # MCP server implementation
│   │   │   ├── tools.py             # MCP tools definition
│   │   │   ├── resources.py         # MCP resources
│   │   │   └── prompts.py           # MCP prompts
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── openfoodfacts.py     # OpenFoodFacts API client
│   │   │   ├── models.py            # Data models
│   │   │   └── cache.py             # API response caching
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── vector_store.py      # Vector database operations
│   │   │   ├── embeddings.py        # Text embeddings
│   │   │   ├── retriever.py         # RAG retrieval logic
│   │   │   └── knowledge_base.py    # Knowledge base management
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── service.py           # Email service abstraction
│   │   │   ├── templates.py         # Email templates
│   │   │   ├── smtp_client.py       # SMTP implementation
│   │   │   └── sendgrid_client.py   # SendGrid implementation
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── nutrition.py         # Nutrition analysis logic
│   │   │   ├── scoring.py           # Health scoring algorithms
│   │   │   ├── recommendations.py   # Product recommendations
│   │   │   └── shopping_list.py     # Shopping list generation
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── helpers.py           # General utilities
│   │   │   ├── validators.py        # Data validation
│   │   │   ├── image_processor.py   # Image processing utilities
│   │   │   └── formatters.py        # Output formatting
│   │   └── exceptions.py            # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── test_mcp/
│   │   ├── __init__.py
│   │   ├── test_server.py
│   │   ├── test_tools.py
│   │   └── test_resources.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_openfoodfacts.py
│   │   └── test_models.py
│   ├── test_rag/
│   │   ├── __init__.py
│   │   ├── test_vector_store.py
│   │   └── test_retriever.py
│   ├── test_email/
│   │   ├── __init__.py
│   │   └── test_service.py
│   ├── test_core/
│   │   ├── __init__.py
│   │   ├── test_nutrition.py
│   │   └── test_scoring.py
│   └── fixtures/
│       ├── sample_products.json
│       └── test_data.py
├── docs/
│   ├── api_reference.md
│   ├── mcp_integration.md
│   ├── deployment.md
│   └── examples.md
├── examples/
│   ├── basic_usage.py
│   ├── mcp_client_example.py
│   └── batch_analysis.py
├── scripts/
│   ├── setup_database.py
│   ├── populate_knowledge_base.py
│   └── generate_test_data.py
├── data/
│   ├── nutrition_guidelines.json
│   ├── allergen_info.json
│   └── dietary_patterns.json
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    └── .dockerignore
```

### Running Tests
```bash
pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Multi-language support
- [ ] Barcode scanning integration
- [ ] Price comparison features
- [ ] Meal planning suggestions
- [ ] Integration with grocery delivery services
- [ ] Mobile app companion

## Support

For questions and support, please open an issue on GitHub or contact [chandan.mohan@gwu.edu](mailto:chandan.mohan@gwu.edu).

---

**EatSmart** - Making food choices smarter, one product at a time! 🥗✨