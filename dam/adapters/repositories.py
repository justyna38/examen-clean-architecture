from typing import List, Optional, Dict
from dam.entities.media import Media
from dam.interfaces.repositories import IMediaRepository

class InMemoryMediaRepository(IMediaRepository):
    def __init__(self):
        self.medias: Dict[str, Media] = {}
    
    def save(self, media: Media) -> Media:
        self.medias[media.id] = media
        return media
    
    def get_by_id(self, media_id: str) -> Optional[Media]:
        return self.medias.get(media_id)
    
    def get_by_ean(self, ean: str) -> List[Media]:
        return [media for media in self.medias.values() if media.ean == ean]