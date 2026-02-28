#!/usr/bin/env python3
"""
Database Manager - Core utilities for enterprise database management

This module provides core functionality for:
- Loading and saving databases
- Schema validation
- Data indexing
- Query operations
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib


class DatabaseManager:
    """Core database management class"""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize database manager
        
        Args:
            base_path: Base path to database directory (defaults to ./database)
        """
        if base_path is None:
            # Get the repository root (enterprise directory)
            current_file = Path(__file__).resolve()
            # utils/db_manager.py -> utils -> database -> repo_root
            repo_root = current_file.parent.parent.parent
            base_path = repo_root / "database"
        
        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.schemas_path = self.base_path / "schemas"
        
        # Ensure directories exist
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.schemas_path.mkdir(parents=True, exist_ok=True)
    
    def load_db(self, db_name: str) -> Dict[str, Any]:
        """Load a database file
        
        Args:
            db_name: Name of database (public_db, internal_db, projects_db, indexed_db)
            
        Returns:
            Database dictionary
        """
        db_file = self.data_path / f"{db_name}.json"
        if not db_file.exists():
            raise FileNotFoundError(f"Database file not found: {db_file}")
        
        with open(db_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_db(self, db_name: str, data: Dict[str, Any]) -> None:
        """Save a database file
        
        Args:
            db_name: Name of database
            data: Database dictionary to save
        """
        db_file = self.data_path / f"{db_name}.json"
        
        # Update timestamp
        data['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        
        # Write atomically
        temp_file = db_file.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        temp_file.replace(db_file)
    
    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load a schema file
        
        Args:
            schema_name: Name of schema (public_schema, internal_schema, projects_schema)
            
        Returns:
            Schema dictionary
        """
        schema_file = self.schemas_path / f"{schema_name}.json"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_record(self, record: Dict[str, Any], schema: Dict[str, Any], db_type: str) -> tuple[bool, List[str]]:
        """Validate a record against schema
        
        Args:
            record: Record to validate
            schema: Schema definition
            db_type: Database type (e.g., 'stakeholders', 'projects')
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        if db_type not in schema['databases']:
            errors.append(f"Unknown database type: {db_type}")
            return False, errors
        
        db_schema = schema['databases'][db_type]
        properties = db_schema['properties']
        
        # Check required fields
        for prop_name, prop_def in properties.items():
            if prop_def.get('required', False) and prop_name not in record:
                errors.append(f"Missing required field: {prop_name}")
        
        # Validate field types and values
        for field, value in record.items():
            if field not in properties:
                # Allow extra fields, just warn
                continue
            
            prop_def = properties[field]
            field_type = prop_def['type']
            
            # Type validation
            if field_type == 'string' and not isinstance(value, str):
                errors.append(f"Field {field} must be a string")
            elif field_type == 'number' and not isinstance(value, (int, float)):
                errors.append(f"Field {field} must be a number")
            elif field_type == 'boolean' and not isinstance(value, bool):
                errors.append(f"Field {field} must be a boolean")
            elif field_type == 'array' and not isinstance(value, list):
                errors.append(f"Field {field} must be an array")
            elif field_type == 'select' and value not in prop_def.get('options', []):
                errors.append(f"Field {field} has invalid value: {value}")
        
        return len(errors) == 0, errors
    
    def add_record(self, db_name: str, db_type: str, record: Dict[str, Any]) -> str:
        """Add a record to a database
        
        Args:
            db_name: Database name (public_db, internal_db, projects_db)
            db_type: Type within database (stakeholders, projects, etc.)
            record: Record to add
            
        Returns:
            Record ID
        """
        # Load database and schema
        db = self.load_db(db_name)
        schema_name = db_name.replace('_db', '_schema')
        schema = self.load_schema(schema_name)
        
        # Generate ID if not present
        if 'id' not in record:
            record['id'] = self._generate_id(db_type, record)
        
        # Add timestamps
        now = datetime.utcnow().isoformat() + 'Z'
        record['created_at'] = now
        record['updated_at'] = now
        
        # Validate
        is_valid, errors = self.validate_record(record, schema, db_type)
        if not is_valid:
            raise ValueError(f"Validation errors: {', '.join(errors)}")
        
        # Add to database
        if db_type not in db:
            db[db_type] = []
        
        db[db_type].append(record)
        
        # Save
        self.save_db(db_name, db)
        
        return record['id']
    
    def update_record(self, db_name: str, db_type: str, record_id: str, updates: Dict[str, Any]) -> bool:
        """Update a record in the database
        
        Args:
            db_name: Database name
            db_type: Type within database
            record_id: ID of record to update
            updates: Fields to update
            
        Returns:
            True if updated, False if not found
        """
        db = self.load_db(db_name)
        
        if db_type not in db:
            return False
        
        for record in db[db_type]:
            if record.get('id') == record_id:
                record.update(updates)
                record['updated_at'] = datetime.utcnow().isoformat() + 'Z'
                self.save_db(db_name, db)
                return True
        
        return False
    
    def query(self, db_name: str, db_type: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query records from database
        
        Args:
            db_name: Database name
            db_type: Type within database
            filters: Optional filters (field: value pairs)
            
        Returns:
            List of matching records
        """
        db = self.load_db(db_name)
        
        if db_type not in db:
            return []
        
        records = db[db_type]
        
        if not filters:
            return records
        
        # Apply filters
        results = []
        for record in records:
            match = True
            for field, value in filters.items():
                if record.get(field) != value:
                    match = False
                    break
            if match:
                results.append(record)
        
        return results
    
    def get_stats(self, db_name: str) -> Dict[str, Any]:
        """Get database statistics
        
        Args:
            db_name: Database name
            
        Returns:
            Statistics dictionary
        """
        db = self.load_db(db_name)
        
        stats = {
            'version': db.get('version'),
            'last_updated': db.get('last_updated'),
            'tables': {}
        }
        
        for key, value in db.items():
            if isinstance(value, list):
                stats['tables'][key] = {
                    'count': len(value)
                }
        
        return stats
    
    def _generate_id(self, db_type: str, record: Dict[str, Any]) -> str:
        """Generate a unique ID for a record
        
        Args:
            db_type: Type of database
            record: Record data
            
        Returns:
            Generated ID
        """
        # Create a hash based on content and timestamp
        content = f"{db_type}_{datetime.utcnow().isoformat()}"
        if 'name' in record:
            content += f"_{record['name']}"
        elif 'title' in record:
            content += f"_{record['title']}"
        elif 'project_name' in record:
            content += f"_{record['project_name']}"
        
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# Singleton instance
_db_manager = None

def get_db_manager() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
