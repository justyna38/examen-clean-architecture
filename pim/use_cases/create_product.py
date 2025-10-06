from typing import Dict, Any
from pim.entities.product import Product
from pim.entities.typology import Typology
from datetime import datetime

class CreateProductUseCase:
    def __init__(self, product_repository, typology_repository):
        self.product_repository = product_repository
        self.typology_repository = typology_repository
    
    def execute(self, ean: str, name: str, typology_name: str, attributes: Dict[str, Any]) -> Product:
        typology = self.typology_repository.get_by_name(typology_name)
        
        for field in typology.fields:
            if field.required and field.name not in attributes:
                raise ValueError(f"Required field {field.name} is missing")
            
            if field.name in attributes:
                if not typology.validate_field(field.name, attributes[field.name]):
                    raise ValueError(f"Invalid value for field {field.name}")
        
        product = Product(
            ean=ean,
            name=name,
            typology=typology_name,
            attributes=attributes,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return self.product_repository.save(product)