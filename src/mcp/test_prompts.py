#!/usr/bin/env python3
"""
Unit tests for GeoMentor Prompts MCP Server functionality
"""

import sys
import os
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / 'server' / 'prompts'))

from prompt_parser import PromptRepository, PromptTemplate
from server.prompts.prompt_server import (
    list_all_prompts, get_prompt_by_title, get_prompts_by_category,
    get_prompts_by_persona, search_prompts, get_repository_stats,
    get_prompt_template_only
)


def test_prompt_parser():
    """Test that prompt parser correctly parses template files"""
    print("Testing prompt parser...")
    
    # Find repository root
    repo_root = Path(__file__).parent.parent.parent
    while not (repo_root / "prompt-templates").exists() and repo_root.parent != repo_root:
        repo_root = repo_root.parent
    
    repo = PromptRepository(str(repo_root))
    
    # Test that we loaded some prompts
    assert len(repo.prompts) > 0, "Should load at least one prompt"
    
    # Test first prompt structure
    first_prompt = repo.prompts[0]
    assert isinstance(first_prompt, PromptTemplate), "Should be PromptTemplate instance"
    assert first_prompt.title, "Should have a title"
    assert first_prompt.category, "Should have a category"
    assert first_prompt.persona, "Should have a persona"
    
    print(f"✓ Loaded {len(repo.prompts)} prompts successfully")


def test_list_all_prompts():
    """Test listing all prompts functionality"""
    print("Testing list all prompts...")
    
    result = list_all_prompts()
    
    assert result["success"] == True, "Should return success"
    assert "total_count" in result, "Should include total count"
    assert "prompts" in result, "Should include prompts list"
    assert result["total_count"] > 0, "Should have at least one prompt"
    assert len(result["prompts"]) == result["total_count"], "Count should match list length"
    
    # Check structure of first prompt
    if result["prompts"]:
        first_prompt = result["prompts"][0]
        assert "title" in first_prompt, "Should have title"
        assert "category" in first_prompt, "Should have category"
        assert "persona" in first_prompt, "Should have persona"
        assert "file_path" in first_prompt, "Should have file_path"
    
    print("✓ List all prompts working correctly")


def test_get_prompt_by_title():
    """Test getting a specific prompt by title"""
    print("Testing get prompt by title...")
    
    # First get list of available prompts
    all_prompts = list_all_prompts()
    
    if all_prompts["prompts"]:
        # Test with existing prompt
        test_title = "Understanding Where"  # We know this exists
        result = get_prompt_by_title(test_title)
        
        assert result["success"] == True, "Should find existing prompt"
        assert "prompt" in result, "Should include prompt data"
        
        prompt = result["prompt"]
        assert "title" in prompt, "Should have title"
        assert "category" in prompt, "Should have category"
        assert "persona" in prompt, "Should have persona"
        assert "objective" in prompt, "Should have objective"
        assert "prompt_template" in prompt, "Should have prompt_template"
        
        # Test with non-existing prompt
        result = get_prompt_by_title("Non-existent Prompt")
        assert result["success"] == False, "Should not find non-existent prompt"
        assert "error" in result, "Should include error message"
        assert "available_titles" in result, "Should list available titles"
    
    print("✓ Get prompt by title working correctly")


def test_get_prompts_by_category():
    """Test filtering prompts by category"""
    print("Testing get prompts by category...")
    
    # Test with known category
    result = get_prompts_by_category("Spatial Analysis")
    
    assert result["success"] == True, "Should return success"
    assert "category" in result, "Should include category"
    assert "count" in result, "Should include count"
    assert "prompts" in result, "Should include prompts"
    assert "available_categories" in result, "Should include available categories"
    
    # Test with non-existent category
    result = get_prompts_by_category("Non-existent Category")
    assert result["count"] == 0, "Should return zero results for non-existent category"
    
    print("✓ Get prompts by category working correctly")


def test_get_prompts_by_persona():
    """Test filtering prompts by persona"""
    print("Testing get prompts by persona...")
    
    # Test with known persona
    result = get_prompts_by_persona("Data Scientist")
    
    assert result["success"] == True, "Should return success"
    assert "persona" in result, "Should include persona"
    assert "count" in result, "Should include count"
    assert "prompts" in result, "Should include prompts"
    assert "available_personas" in result, "Should include available personas"
    
    print("✓ Get prompts by persona working correctly")


def test_search_prompts():
    """Test search functionality"""
    print("Testing search prompts...")
    
    # Test with general search term
    result = search_prompts("spatial")
    
    assert result["success"] == True, "Should return success"
    assert "query" in result, "Should include query"
    assert "count" in result, "Should include count"
    assert "prompts" in result, "Should include prompts"
    
    # Test with specific search term that should match
    result = search_prompts("mapping")
    assert result["count"] >= 0, "Should handle search query"
    
    print("✓ Search prompts working correctly")


def test_get_repository_stats():
    """Test repository statistics"""
    print("Testing repository stats...")
    
    result = get_repository_stats()
    
    assert result["success"] == True, "Should return success"
    assert "statistics" in result, "Should include statistics"
    
    stats = result["statistics"]
    assert "total_prompts" in stats, "Should include total prompts"
    assert "categories" in stats, "Should include categories"
    assert "personas" in stats, "Should include personas"
    assert "category_counts" in stats, "Should include category counts"
    assert "persona_counts" in stats, "Should include persona counts"
    
    assert stats["total_prompts"] > 0, "Should have at least one prompt"
    assert len(stats["categories"]) > 0, "Should have at least one category"
    assert len(stats["personas"]) > 0, "Should have at least one persona"
    
    print("✓ Repository stats working correctly")


def test_get_prompt_template_only():
    """Test getting just the prompt template text"""
    print("Testing get prompt template only...")
    
    result = get_prompt_template_only("Understanding Where")
    
    assert result["success"] == True, "Should find existing prompt"
    assert "title" in result, "Should include title"
    assert "prompt_template" in result, "Should include prompt template"
    assert "usage_instructions" in result, "Should include usage instructions"
    
    # Test with non-existent prompt
    result = get_prompt_template_only("Non-existent Prompt")
    assert result["success"] == False, "Should not find non-existent prompt"
    
    print("✓ Get prompt template only working correctly")


def test_prompt_structure():
    """Test that prompts have expected structure"""
    print("Testing prompt structure...")
    
    all_prompts = list_all_prompts()
    
    if all_prompts["prompts"]:
        # Get full prompt details
        first_title = all_prompts["prompts"][0]["title"]
        prompt_result = get_prompt_by_title(first_title)
        
        if prompt_result["success"]:
            prompt = prompt_result["prompt"]
            
            # Verify all expected fields are present
            expected_fields = [
                "title", "category", "persona", "objective", 
                "prompt_template", "usage_instructions", "example_use_cases"
            ]
            
            for field in expected_fields:
                assert field in prompt, f"Prompt should have {field} field"
            
            # Verify example_use_cases is a list
            assert isinstance(prompt["example_use_cases"], list), "Example use cases should be a list"
    
    print("✓ Prompt structure validation working correctly")


def main():
    """Run all tests"""
    print("Running GeoMentor Prompts MCP Server tests...\n")
    
    try:
        test_prompt_parser()
        test_list_all_prompts()
        test_get_prompt_by_title()
        test_get_prompts_by_category()
        test_get_prompts_by_persona()
        test_search_prompts()
        test_get_repository_stats()
        test_get_prompt_template_only()
        test_prompt_structure()
        
        print("\n✅ All tests passed! GeoMentor Prompts MCP Server is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())