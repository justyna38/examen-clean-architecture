import os
from typing import Dict
from dam.interfaces.services import IMediaStorage, IProductLinker

class FileSystemMediaStorage(IMediaStorage):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def store(self, media) -> str:
        file_path = os.path.join(self.storage_path, media.filename)
        with open(file_path, 'wb') as f:
            f.write(b"dummy content")
        return file_path
    
    def retrieve(self, media_id: str) -> bytes:
        file_path = os.path.join(self.storage_path, media_id)
        with open(file_path, 'rb') as f:
            return f.read()

class InMemoryProductLinker(IProductLinker):
    def __init__(self):
        self.links: Dict[str, list] = {}
    
    def link_media_to_product(self, ean: str, sku: str, media_id: str) -> None:
        key = f"{ean}_{sku}"
        if key not in self.links:
            self.links[key] = []
        self.links[key].append(media_id)
    
    def get_media_for_product(self, ean: str) -> list:
        result = []
        for key, media_ids in self.links.items():
            if key.startswith(ean):
                result.extend(media_ids)
        return result