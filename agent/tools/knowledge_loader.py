import os
import json

ENTRIES = "entries"
TTILE = "title"
DETAIL = "detail"

def load_knowledge_base():
    """Load knowledge base from JSON file"""
    knowledge_base_path = os.path.join(os.path.dirname("data-source/knowledge_base.json"))
    try:
        with open(knowledge_base_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Knowledge base file not found at: {knowledge_base_path}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in knowledge base file")
    
def get_all_titles():
    """
    Get all titles from the knowledge base.
    
    Returns:
        list[str]: List of all titles in the knowledge base
        
    Raises:
        FileNotFoundError: If knowledge base file is not found
        json.JSONDecodeError: If JSON format is invalid
    """
    try:
        data = load_knowledge_base()
        print("data: ", data.get(ENTRIES, []))
        
        # Extract all titles from entries
        titles = [item.get("title", "") for item in data.get("entries", [])]
        return titles if titles else ["No titles found."]
        
    except Exception as e:
        print(f"Error loading knowledge base: {str(e)}")
        return []
    
def search_titles_and_details(search_query: str) -> list[dict[str, str]]:
    """
    Get titles and details that match the search query.
    
    Args:
        search_query (str): Text to search for in titles
        
    Returns:
        list[dict[str, str]]: List of matching entries with title and detail
            Format: [{"title": "...", "detail": "..."}, ...]
            
    Raises:
        FileNotFoundError: If knowledge base file is not found
        json.JSONDecodeError: If JSON format is invalid
    """
    try:
        with open("data-source/knowledge_base.json", "r") as f:
            knowledge_base = json.load(f)

        print("knowledge_base: ", knowledge_base.get(ENTRIES, []))

        matched_entries = []
        for entry in knowledge_base.get(ENTRIES, []):
            title = entry.get(TTILE, "").lower()
            if title in search_query.lower():
                matched_entries.append({TTILE: entry.get(TTILE, ""), DETAIL: entry.get(DETAIL, "")})

        return matched_entries
        
    except Exception as e:
        print(f"Error searching knowledge base: {str(e)}")
        return []