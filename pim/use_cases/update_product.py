from typing import Dict, Any

class UpdateProductUseCase:
    def __init__(self, product_repository, typology_repository):
        self.product_repository = product_repository
        self.typology_repository = typology_repository
    
    def execute(self, ean: str, attributes: Dict[str, Any]) -> None:
        product = self.product_repository.get_by_ean(ean)
        if not product:
            raise ValueError(f"Product with EAN {ean} not found")
        
        typology = self.typology_repository.get_by_name(product.typology)
        
        for field_name, value in attributes.items():
            if not typology.validate_field(field_name, value):
                raise ValueError(f"Invalid value for field {field_name}")
            product.update_attribute(field_name, value)
        
        self.product_repository.save(product)