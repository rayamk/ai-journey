import json
import os
from datetime import datetime
from typing import List, Dict, Any

class DataManager:
    """Simple data storage manager"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "history.json")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_history(self, history: List[Dict[str, Any]]):
        """Save history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except IOError:
            pass
    
    def add_entry(self, entry: Dict[str, Any]):
        """Add a new entry to history"""
        history = self._load_history()
        # Add timestamp
        entry_with_time = entry.copy()
        entry_with_time['timestamp'] = datetime.now().isoformat()
        history.insert(0, entry_with_time)  # Add at the beginning
        # Keep only last 50 entries
        if len(history) > 50:
            history = history[:50]
        self._save_history(history)
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent history entries"""
        history = self._load_history()
        return history[:limit]
    
    def clear_history(self):
        """Clear all history"""
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)
            except IOError:
                pass

data_manager = DataManager()
