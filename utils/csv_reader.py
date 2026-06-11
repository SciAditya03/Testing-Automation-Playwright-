import csv
from pathlib import Path
from typing import List, Dict

class CSVTestCaseReader:
    """Read test cases from CSV file into list of dictionaries"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def read_all(self) -> List[Dict[str, str]]:
        """Read all rows as list of dicts"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Test case file not found: {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def filter_by_priority(self, priority: str) -> List[Dict[str, str]]:
        """Filter test cases by priority (smoke/regression/edge)"""
        all_cases = self.read_all()
        return [case for case in all_cases if case['priority'].lower() == priority.lower()]
    
    def filter_by_module(self, module: str) -> List[Dict[str, str]]:
        """Filter test cases by module (Feed/Chats/Integration)"""
        all_cases = self.read_all()
        return [case for case in all_cases if case['module'].lower() == module.lower()]
    
    def get_test_ids(self) -> List[str]:
        """Return list of all test IDs for reporting"""
        return [case['test_id'] for case in self.read_all()]