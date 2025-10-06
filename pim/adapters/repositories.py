from typing import List, Optional, Dict
from pim.entities.product import Product
from pim.entities.typology import Typology
from pim.interfaces.repositories import IProductRepository, ITypologyRepository

class InMemoryProductRepository(IProductRepository):
    def __init__(self):
        self.products: Dict[str, Product] = {}
    
    def save(self, product: Product) -> Product:
        self.products[product.ean] = product
        return product
    
    def get_by_ean(self, ean: str) -> Optional[Product]:
        return self.products.get(ean)
    
    def get_all(self) -> List[Product]:
        return list(self.products.values())

class InMemoryTypologyRepository(ITypologyRepository):
    def __init__(self):
        self.typologies: Dict[str, Typology] = {}
    
    def save(self, typology: Typology) -> Typology:
        self.typologies[typology.name] = typology
        return typology
    
    def get_by_name(self, name: str) -> Optional[Typology]:
        return self.typologies.get(name)
    
    def get_all(self) -> List[Typology]:
        return list(self.typologies.values())