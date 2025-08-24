import unittest
from unittest.mock import mock_open, patch
import json
import os
import sys

# Add src/ to sys.path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../src")))

from agent.tools.knowledge_loader import load_knowledge_base, get_all_titles, search_titles_and_details, KNOWLEDGE_SOURCE, ENTRIES, TTILE, DETAIL

class TestKnowledgeBase(unittest.TestCase):
    def setUp(self):
        # Sample knowledge base data
        self.sample_knowledge_base = {
            ENTRIES: [
                {TTILE: "Python Basics", DETAIL: "Introduction to Python programming"},
                {TTILE: "Data Science", DETAIL: "Overview of data science concepts"},
                {TTILE: "Machine Learning", DETAIL: "Basics of ML algorithms"}
            ]
        }
        self.sample_json = json.dumps(self.sample_knowledge_base)
        self.invalid_json = "{invalid json}"

    @patch('builtins.open', new_callable=mock_open)
    def test_load_knowledge_base_success(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.sample_json
        
        # Act
        result = load_knowledge_base()
        
        # Assert
        self.assertEqual(result, self.sample_knowledge_base)
        mock_file.assert_called_once_with(os.path.join(os.path.dirname(KNOWLEDGE_SOURCE)), 'r')

    @patch('builtins.open', new_callable=mock_open)
    def test_load_knowledge_base_file_not_found(self, mock_file):
        # Arrange
        mock_file.side_effect = FileNotFoundError("File not found")
        
        # Act/Assert
        with self.assertRaises(FileNotFoundError) as cm:
            load_knowledge_base()
        self.assertTrue(str(cm.exception).startswith("Knowledge base file not found at"))

    @patch('builtins.open', new_callable=mock_open)
    def test_load_knowledge_base_invalid_json(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.invalid_json
        
        # Act/Assert
        with self.assertRaises(ValueError) as cm:
            load_knowledge_base()
        self.assertEqual(str(cm.exception), "Invalid JSON format in knowledge base file")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_all_titles_success(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.sample_json
        
        # Act
        result = get_all_titles()
        
        # Assert
        expected_titles = ["Python Basics", "Data Science", "Machine Learning"]
        self.assertEqual(result, expected_titles)
        mock_file.assert_called_once_with(KNOWLEDGE_SOURCE, "r")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_all_titles_empty_entries(self, mock_file):
        # Arrange
        empty_knowledge_base = {ENTRIES: []}
        mock_file.return_value.read.return_value = json.dumps(empty_knowledge_base)
        
        # Act
        result = get_all_titles()
        
        # Assert
        self.assertEqual(result, ["No titles found."])

    @patch('builtins.open', new_callable=mock_open)
    def test_get_all_titles_file_not_found(self, mock_file):
        # Arrange
        mock_file.side_effect = FileNotFoundError("File not found")
        
        # Act
        result = get_all_titles()
        
        # Assert
        self.assertEqual(result, [])
        mock_file.assert_called_once_with(KNOWLEDGE_SOURCE, "r")

    @patch('builtins.open', new_callable=mock_open)
    def test_get_all_titles_invalid_json(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.invalid_json
        
        # Act
        result = get_all_titles()
        
        # Assert
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_search_titles_and_details_success(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.sample_json
        search_query = "Python Basics"
        
        # Act
        result = search_titles_and_details(search_query)
        
        # Assert
        expected_result = [
            {TTILE: "Python Basics", DETAIL: "Introduction to Python programming"}
        ]
        self.assertEqual(result, expected_result)
        mock_file.assert_called_once_with(KNOWLEDGE_SOURCE, "r")

    @patch('builtins.open', new_callable=mock_open)
    def test_search_titles_and_details_no_match(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.sample_json
        search_query = "Nonexistent Topic"
        
        # Act
        result = search_titles_and_details(search_query)
        
        # Assert
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_search_titles_and_details_empty_entries(self, mock_file):
        # Arrange
        empty_knowledge_base = {ENTRIES: []}
        mock_file.return_value.read.return_value = json.dumps(empty_knowledge_base)
        search_query = "Python Basics"
        
        # Act
        result = search_titles_and_details(search_query)
        
        # Assert
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_search_titles_and_details_file_not_found(self, mock_file):
        # Arrange
        mock_file.side_effect = FileNotFoundError("File not found")
        
        # Act
        result = search_titles_and_details("Python Basics")
        
        # Assert
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_search_titles_and_details_invalid_json(self, mock_file):
        # Arrange
        mock_file.return_value.read.return_value = self.invalid_json
        
        # Act
        result = search_titles_and_details("Python Basics")
        
        # Assert
        self.assertEqual(result, [])