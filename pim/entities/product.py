from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime

@dataclass
class Product:
    ean: str
    name: str
    typology: str
    attributes: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    def update_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value
        self.updated_at = datetime.now()
    
    def get_attribute(self, key: str) -> Any:
        return self.attributes.get(key)