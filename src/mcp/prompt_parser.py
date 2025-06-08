#!/usr/bin/env python3
"""
Prompt Template Parser for GeoMentor Prompts
Parses markdown files in the prompt-templates directory and extracts structured data
"""

import os
import re
from typing import Dict, List, Optional
from pathlib import Path


class PromptTemplate:
    """Represents a parsed prompt template"""
    
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content
        self.title = self._extract_title()
        self.category = self._extract_category()
        self.persona = self._extract_persona()
        self.objective = self._extract_objective()
        self.prompt_template = self._extract_prompt_template()
        self.usage_instructions = self._extract_usage_instructions()
        self.example_use_cases = self._extract_example_use_cases()
        
    def _extract_title(self) -> str:
        """Extract title from the first heading"""
        match = re.search(r'^# (.+)$', self.content, re.MULTILINE)
        return match.group(1).strip() if match else "Untitled"
    
    def _extract_category(self) -> str:
        """Extract category from the category section"""
        match = re.search(r'## 🏷️ \*\*Category:\*\* (.+)', self.content)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_persona(self) -> str:
        """Extract persona from the persona section"""
        match = re.search(r'## 👤 \*\*Persona:\*\* (.+)', self.content)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_objective(self) -> str:
        """Extract objective section"""
        match = re.search(r'### 🎯 \*\*Objective\*\*\n(.+?)(?=\n###|\n##|\Z)', self.content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_prompt_template(self) -> str:
        """Extract the prompt template section"""
        match = re.search(r'### 📝 \*\*Prompt Template\*\*(.+?)(?=\n###|\n##|\Z)', self.content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_usage_instructions(self) -> str:
        """Extract usage instructions"""
        match = re.search(r'#### 🔧 Usage Instructions:(.+?)(?=\n####|\n###|\n##|\Z)', self.content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_example_use_cases(self) -> List[str]:
        """Extract example use cases as a list"""
        match = re.search(r'### 💡 \*\*Example Use Cases:\*\*(.+?)(?=\n###|\n##|\Z)', self.content, re.DOTALL)
        if not match:
            return []
        
        use_cases_text = match.group(1).strip()
        # Extract bullet points
        use_cases = re.findall(r'^- (.+)$', use_cases_text, re.MULTILINE)
        return [case.strip() for case in use_cases]
    
    def to_dict(self) -> Dict:
        """Convert prompt template to dictionary"""
        return {
            "file_path": self.file_path,
            "title": self.title,
            "category": self.category,
            "persona": self.persona,
            "objective": self.objective,
            "prompt_template": self.prompt_template,
            "usage_instructions": self.usage_instructions,
            "example_use_cases": self.example_use_cases,
            "content": self.content
        }


class PromptRepository:
    """Repository for managing prompt templates"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.prompts: List[PromptTemplate] = []
        self._load_prompts()
    
    def _load_prompts(self):
        """Load all prompt templates from the repository"""
        self.prompts = []
        prompt_templates_path = self.base_path / "prompt-templates"
        
        if not prompt_templates_path.exists():
            return
        
        # Find all markdown files in the prompt-templates directory
        for md_file in prompt_templates_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    prompt = PromptTemplate(str(md_file), content)
                    self.prompts.append(prompt)
            except Exception as e:
                print(f"Warning: Failed to parse {md_file}: {e}")
    
    def get_all_prompts(self) -> List[Dict]:
        """Get all prompts as dictionaries"""
        return [prompt.to_dict() for prompt in self.prompts]
    
    def get_prompts_by_category(self, category: str) -> List[Dict]:
        """Get prompts filtered by category"""
        return [prompt.to_dict() for prompt in self.prompts 
                if category.lower() in prompt.category.lower()]
    
    def get_prompts_by_persona(self, persona: str) -> List[Dict]:
        """Get prompts filtered by persona"""
        return [prompt.to_dict() for prompt in self.prompts 
                if persona.lower() in prompt.persona.lower()]
    
    def search_prompts(self, query: str) -> List[Dict]:
        """Search prompts by keywords in title, objective, or use cases"""
        query_lower = query.lower()
        results = []
        
        for prompt in self.prompts:
            # Search in title, objective, and use cases
            search_text = f"{prompt.title} {prompt.objective} {' '.join(prompt.example_use_cases)}"
            if query_lower in search_text.lower():
                results.append(prompt.to_dict())
        
        return results
    
    def get_prompt_by_title(self, title: str) -> Optional[Dict]:
        """Get a specific prompt by title"""
        for prompt in self.prompts:
            if title.lower() in prompt.title.lower():
                return prompt.to_dict()
        return None
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set(prompt.category for prompt in self.prompts)
        return sorted(list(categories))
    
    def get_personas(self) -> List[str]:
        """Get all unique personas"""
        personas = set(prompt.persona for prompt in self.prompts)
        return sorted(list(personas))
    
    def get_stats(self) -> Dict:
        """Get repository statistics"""
        return {
            "total_prompts": len(self.prompts),
            "categories": self.get_categories(),
            "personas": self.get_personas(),
            "category_counts": {cat: len(self.get_prompts_by_category(cat)) for cat in self.get_categories()},
            "persona_counts": {persona: len(self.get_prompts_by_persona(persona)) for persona in self.get_personas()}
        }