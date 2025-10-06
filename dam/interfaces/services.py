from abc import ABC, abstractmethod

class IMediaStorage(ABC):
    @abstractmethod
    def store(self, media) -> str:
        pass
    
    @abstractmethod
    def retrieve(self, media_id: str) -> bytes:
        pass

class IProductLinker(ABC):
    @abstractmethod
    def link_media_to_product(self, ean: str, sku: str, media_id: str) -> None:
        pass
    
    @abstractmethod
    def get_media_for_product(self, ean: str) -> list:
        pass