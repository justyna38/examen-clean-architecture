from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class FieldDefinition:
    name: str
    field_type: str
    required: bool
    validation_rules: Dict[str, Any]

@dataclass
class Typology:
    name: str
    fields: List[FieldDefinition]
    
    def get_field_definition(self, field_name: str) -> FieldDefinition:
        for field in self.fields:
            if field.name == field_name:
                return field
        raise ValueError(f"Field {field_name} not found in typology {self.name}")
    
    def validate_field(self, field_name: str, value: Any) -> bool:
        field_def = self.get_field_definition(field_name)
        if field_def.required and value is None:
            return False
        return True