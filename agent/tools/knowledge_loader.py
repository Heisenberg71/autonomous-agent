import os
import json

ENTRIES = "entries"
TTILE = "title"
DETAIL = "detail"
KNOWLEDGE_SOURCE = "data/knowledge_base.json"

def load_knowledge_base():
    """
    Load the knowledge base from a JSON file.

    Returns:
        dict: Parsed contents of the knowledge base.

    Raises:
        FileNotFoundError: If the JSON file is not found at the specified path.
        ValueError: If the file content is not valid JSON.
    """
    knowledge_base_path = os.path.join(os.path.dirname(KNOWLEDGE_SOURCE))
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
        with open(KNOWLEDGE_SOURCE, "r") as f:
            knowledge_base = json.load(f)

        print("knowledge_base: ", knowledge_base.get(ENTRIES, []))
        
        # Extract all titles from entries
        titles = [entry.get(TTILE, "") for entry in knowledge_base.get(ENTRIES, [])]
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
        with open(KNOWLEDGE_SOURCE, "r") as f:
            knowledge_base = json.load(f)

        print("search Query: ", search_query)

        matched_entries = []
        for entry in knowledge_base.get(ENTRIES, []):
            title = entry.get(TTILE, "")
            if title in search_query:
                matched_entries.append({TTILE: entry.get(TTILE, ""), DETAIL: entry.get(DETAIL, "")})

        return matched_entries
        
    except Exception as e:
        print(f"Error searching knowledge base: {str(e)}")
        return []