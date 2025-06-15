# GeoMentor Prompts MCP Server Documentation

## Overview
The GeoMentor Prompts MCP Server provides programmatic access to all geospatial AI prompt templates in the repository through the Model Context Protocol (MCP). This allows AI assistants and applications to discover, search, and utilize specialized geospatial prompts for various use cases.

## Features
- **Comprehensive Prompt Access**: Access to all prompt templates across categories and personas
- **Intelligent Search**: Search prompts by keywords, category, or persona
- **Structured Data**: Well-formatted prompt data with metadata
- **MCP Integration**: Full MCP compliance with tools and resources
- **Real-time Updates**: Automatically reflects changes in the prompt repository

## Architecture

### Components
1. **PromptRepository**: Core class that parses and manages prompt templates
2. **PromptTemplate**: Data structure representing individual prompts
3. **Prompt MCP Server**: FastMCP server exposing prompts through tools and resources
4. **Test Suite**: Comprehensive tests ensuring functionality

### File Structure
```
src/mcp/
├── prompt_parser.py          # Core prompt parsing logic
├── server/prompts/
│   └── prompt_server.py      # MCP server implementation
├── test_prompts.py           # Unit tests for prompt functionality
└── PROMPTS.md               # This documentation file
```

## Tools Available

### `list_all_prompts()`
Lists all available prompt templates with metadata.

**Returns:**
```json
{
    "success": true,
    "total_count": 8,
    "prompts": [
        {
            "title": "🌍 Understanding Where",
            "category": "Spatial Analysis",
            "persona": "Data Scientist",
            "file_path": "/path/to/prompt.md"
        }
    ]
}
```

### `get_prompt_by_title(title: str)`
Retrieves a specific prompt template by title (supports partial matching).

**Parameters:**
- `title` (str): The title or partial title of the prompt

**Returns:**
Complete prompt template with all sections including objectives, usage instructions, and example use cases.

### `get_prompts_by_category(category: str)`
Filters prompts by category (e.g., "Spatial Analysis", "Image Analysis").

**Parameters:**
- `category` (str): The category to filter by

**Returns:**
List of prompts matching the specified category.

### `get_prompts_by_persona(persona: str)`
Filters prompts by target persona (e.g., "Data Scientist", "Intelligence Analyst").

**Parameters:**
- `persona` (str): The persona to filter by

**Returns:**
List of prompts designed for the specified persona.

### `search_prompts(query: str)`
Searches prompts by keywords in title, objective, or use cases.

**Parameters:**
- `query` (str): Search keywords

**Returns:**
List of prompts matching the search query.

### `get_repository_stats()`
Provides statistics about the prompt repository.

**Returns:**
```json
{
    "success": true,
    "statistics": {
        "total_prompts": 8,
        "categories": ["Spatial Analysis", "Image Analysis", "Geospatial Intelligence"],
        "personas": ["Data Scientist", "Intelligence Analyst"],
        "category_counts": {"Spatial Analysis": 6, "Image Analysis": 1, "Geospatial Intelligence": 1},
        "persona_counts": {"Data Scientist": 7, "Intelligence Analyst": 1}
    }
}
```

### `get_prompt_template_only(title: str)`
Returns only the prompt template text for immediate use.

**Parameters:**
- `title` (str): The title or partial title of the prompt

**Returns:**
Streamlined response with just the prompt template and usage instructions.

## Resources Available

### `prompt://{title}`
Direct access to a formatted prompt template.

**Example:** `prompt://Understanding Where`

Returns a well-formatted prompt template ready for use.

### `prompts://category/{category}`
List all prompts in a specific category.

**Example:** `prompts://category/Spatial Analysis`

Returns formatted overview of all prompts in the category.

### `prompts://persona/{persona}`
List all prompts for a specific persona.

**Example:** `prompts://persona/Data Scientist`

Returns formatted overview of all prompts designed for the persona.

## Usage Examples

### Basic Prompt Discovery
```python
# List all available prompts
all_prompts = list_all_prompts()
print(f"Found {all_prompts['total_count']} prompts")

# Get prompts for data scientists
ds_prompts = get_prompts_by_persona("Data Scientist")
for prompt in ds_prompts['prompts']:
    print(f"- {prompt['title']} ({prompt['category']})")
```

### Searching and Retrieving Prompts
```python
# Search for mapping-related prompts
mapping_prompts = search_prompts("mapping")
print(f"Found {mapping_prompts['count']} mapping-related prompts")

# Get a specific prompt
understanding_where = get_prompt_by_title("Understanding Where")
if understanding_where['success']:
    prompt = understanding_where['prompt']
    print(f"Title: {prompt['title']}")
    print(f"Objective: {prompt['objective']}")
```

### Using Prompt Templates
```python
# Get just the template text for immediate use
template = get_prompt_template_only("Making Predictions")
if template['success']:
    print("Prompt Template:")
    print(template['prompt_template'])
    print("\nUsage Instructions:")
    print(template['usage_instructions'])
```

## Prompt Template Structure

Each prompt template includes:

- **Title**: Descriptive name with emoji
- **Category**: Main classification (e.g., Spatial Analysis)
- **Persona**: Target user type (e.g., Data Scientist)
- **Objective**: Clear description of the prompt's purpose
- **Prompt Template**: Structured AI agent tasks and instructions
- **Usage Instructions**: Step-by-step guide for using the prompt
- **Example Use Cases**: Real-world applications and scenarios

## Categories and Personas

### Current Categories
- **Spatial Analysis**: Geospatial data analysis and pattern recognition
- **Image Analysis**: Remote sensing and geospatial imagery processing
- **Geospatial Intelligence**: Intelligence analysis with spatial components

### Current Personas
- **Data Scientist**: Technical professionals working with geospatial data
- **Intelligence Analyst**: Professionals in intelligence and security domains

## Testing

The prompt server includes comprehensive unit tests covering:

- Prompt parsing and structure validation
- All MCP tools functionality
- Search and filtering capabilities
- Error handling and edge cases
- Resource endpoints

Run tests with:
```bash
python src/mcp/test_prompts.py
```

## Server Startup

Start the MCP server:
```bash
python src/mcp/server/prompts/prompt_server.py
```

The server will be available at `http://127.0.0.1:8001` with SSE transport.

## Integration with Existing MCP Infrastructure

The prompt server complements the existing location-based MCP server and can run alongside it on different ports. Both servers follow the same MCP patterns and can be used together for comprehensive geospatial AI assistance.

## Error Handling

The server provides robust error handling:
- Graceful handling of missing prompts
- Clear error messages with helpful suggestions
- Validation of search parameters
- Fallback responses for edge cases

## Performance Considerations

- Prompts are loaded once at startup for fast access
- In-memory storage for quick search and retrieval
- Minimal overhead for MCP protocol compliance
- Efficient parsing of markdown templates

## Future Enhancements

Planned improvements include:
- Dynamic prompt reloading without server restart
- Advanced search with fuzzy matching
- Prompt versioning and change tracking
- Integration with prompt generation tools
- Extended metadata and tagging system