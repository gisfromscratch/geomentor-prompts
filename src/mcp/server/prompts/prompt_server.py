#!/usr/bin/env python3
"""
GeoMentor Prompts MCP Server
Provides access to geospatial AI prompt templates through MCP (Model Context Protocol)
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add the parent directory to the path to import prompt_parser
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent))

from mcp.server.fastmcp import FastMCP
from prompt_parser import PromptRepository

# Get the repository root path (go up to find the repo root)
REPO_ROOT = Path(__file__).parent.parent.parent.parent
# Ensure we're at the actual repository root (contains prompt-templates)
while not (REPO_ROOT / "prompt-templates").exists() and REPO_ROOT.parent != REPO_ROOT:
    REPO_ROOT = REPO_ROOT.parent

prompt_repo = PromptRepository(str(REPO_ROOT))

# Create an MCP server for prompts
mcp = FastMCP(name="GeoMentor Prompts MCP Server", 
              description="Provides access to geospatial AI prompt templates and tools",
              version="1.0.0",
              port=8001)


@mcp.tool()
def list_all_prompts() -> Dict:
    """
    List all available prompt templates in the repository
    
    Returns:
        Dictionary containing all prompt templates with metadata
    """
    prompts = prompt_repo.get_all_prompts()
    
    return {
        "success": True,
        "total_count": len(prompts),
        "prompts": [{
            "title": p["title"],
            "category": p["category"],
            "persona": p["persona"],
            "file_path": p["file_path"]
        } for p in prompts]
    }


@mcp.tool()
def get_prompt_by_title(title: str) -> Dict:
    """
    Get a specific prompt template by title
    
    Args:
        title: The title or partial title of the prompt to retrieve
        
    Returns:
        Complete prompt template with all sections
    """
    prompt = prompt_repo.get_prompt_by_title(title)
    
    if prompt:
        return {
            "success": True,
            "prompt": prompt
        }
    else:
        return {
            "success": False,
            "error": f"No prompt found with title containing: {title}",
            "available_titles": [p["title"] for p in prompt_repo.get_all_prompts()]
        }


@mcp.tool()
def get_prompts_by_category(category: str) -> Dict:
    """
    Get all prompts filtered by category
    
    Args:
        category: The category to filter by (e.g., 'Spatial Analysis', 'Image Analysis')
        
    Returns:
        List of prompts matching the category
    """
    prompts = prompt_repo.get_prompts_by_category(category)
    
    return {
        "success": True,
        "category": category,
        "count": len(prompts),
        "prompts": prompts,
        "available_categories": prompt_repo.get_categories()
    }


@mcp.tool()
def get_prompts_by_persona(persona: str) -> Dict:
    """
    Get all prompts filtered by persona/user type
    
    Args:
        persona: The persona to filter by (e.g., 'Data Scientist', 'Intelligence Analyst')
        
    Returns:
        List of prompts matching the persona
    """
    prompts = prompt_repo.get_prompts_by_persona(persona)
    
    return {
        "success": True,
        "persona": persona,
        "count": len(prompts),
        "prompts": prompts,
        "available_personas": prompt_repo.get_personas()
    }


@mcp.tool()
def search_prompts(query: str) -> Dict:
    """
    Search prompts by keywords in title, objective, or use cases
    
    Args:
        query: Search keywords
        
    Returns:
        List of prompts matching the search query
    """
    prompts = prompt_repo.search_prompts(query)
    
    return {
        "success": True,
        "query": query,
        "count": len(prompts),
        "prompts": prompts
    }


@mcp.tool()
def get_repository_stats() -> Dict:
    """
    Get statistics about the prompt repository
    
    Returns:
        Statistics including counts by category and persona
    """
    stats = prompt_repo.get_stats()
    
    return {
        "success": True,
        "statistics": stats
    }


@mcp.tool()
def get_prompt_template_only(title: str) -> Dict:
    """
    Get only the prompt template section (without metadata) for direct use
    
    Args:
        title: The title or partial title of the prompt
        
    Returns:
        Just the prompt template text for immediate use
    """
    prompt = prompt_repo.get_prompt_by_title(title)
    
    if prompt:
        return {
            "success": True,
            "title": prompt["title"],
            "prompt_template": prompt["prompt_template"],
            "usage_instructions": prompt["usage_instructions"]
        }
    else:
        return {
            "success": False,
            "error": f"No prompt found with title containing: {title}",
            "available_titles": [p["title"] for p in prompt_repo.get_all_prompts()]
        }


# MCP Resources for accessing prompts
@mcp.resource("prompt://{title}")
def get_prompt_resource(title: str) -> str:
    """
    Get a prompt template as a resource
    
    Args:
        title: The title of the prompt to retrieve
        
    Returns:
        Formatted prompt template text
    """
    prompt = prompt_repo.get_prompt_by_title(title)
    
    if prompt:
        return f"""# {prompt['title']}

**Category:** {prompt['category']}
**Persona:** {prompt['persona']}

## Objective
{prompt['objective']}

## Prompt Template
{prompt['prompt_template']}

## Usage Instructions
{prompt['usage_instructions']}

## Example Use Cases
{chr(10).join(f"- {case}" for case in prompt['example_use_cases'])}
"""
    else:
        return f"Error: No prompt found with title containing '{title}'"


@mcp.resource("prompts://category/{category}")
def get_category_prompts_resource(category: str) -> str:
    """
    Get all prompts for a category as a resource
    
    Args:
        category: The category name
        
    Returns:
        Formatted list of prompts in the category
    """
    prompts = prompt_repo.get_prompts_by_category(category)
    
    if prompts:
        output = f"# {category} Prompts\n\n"
        for prompt in prompts:
            output += f"## {prompt['title']}\n"
            output += f"**Persona:** {prompt['persona']}\n"
            output += f"**Objective:** {prompt['objective'][:100]}...\n\n"
        return output
    else:
        available_categories = prompt_repo.get_categories()
        return f"Error: No prompts found for category '{category}'. Available categories: {', '.join(available_categories)}"


@mcp.resource("prompts://persona/{persona}")
def get_persona_prompts_resource(persona: str) -> str:
    """
    Get all prompts for a persona as a resource
    
    Args:
        persona: The persona name
        
    Returns:
        Formatted list of prompts for the persona
    """
    prompts = prompt_repo.get_prompts_by_persona(persona)
    
    if prompts:
        output = f"# {persona} Prompts\n\n"
        for prompt in prompts:
            output += f"## {prompt['title']}\n"
            output += f"**Category:** {prompt['category']}\n"
            output += f"**Objective:** {prompt['objective'][:100]}...\n\n"
        return output
    else:
        available_personas = prompt_repo.get_personas()
        return f"Error: No prompts found for persona '{persona}'. Available personas: {', '.join(available_personas)}"


if __name__ == "__main__":
    # Start the server locally
    print(f"Starting GeoMentor Prompts MCP Server...")
    print(f"Repository loaded with {len(prompt_repo.prompts)} prompts")
    print(f"Categories: {prompt_repo.get_categories()}")
    print(f"Personas: {prompt_repo.get_personas()}")
    mcp.run(transport="sse")