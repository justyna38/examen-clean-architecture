from abc import ABC, abstractmethod
from typing import List, Optional
from dam.entities.media import Media

class IMediaRepository(ABC):
    @abstractmethod
    def save(self, media: Media) -> Media:
        pass
    
    @abstractmethod
    def get_by_id(self, media_id: str) -> Optional[Media]:
        pass
    
    @abstractmethod
    def get_by_ean(self, ean: str) -> List[Media]:
        pass