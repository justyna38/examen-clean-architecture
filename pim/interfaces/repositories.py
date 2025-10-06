from abc import ABC, abstractmethod
from typing import List, Optional
from pim.entities.product import Product
from pim.entities.typology import Typology

class IProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def get_by_ean(self, ean: str) -> Optional[Product]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

class ITypologyRepository(ABC):
    @abstractmethod
    def save(self, typology: Typology) -> Typology:
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Typology]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Typology]:
        pass