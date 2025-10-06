from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"

@dataclass
class Media:
    id: str
    filename: str
    media_type: MediaType
    file_path: str
    ean: Optional[str]
    sku: Optional[str]
    created_at: datetime
    
    @classmethod
    def from_filename(cls, filename: str, file_path: str) -> 'Media':
        parts = filename.split('_')
        ean = parts[0] if len(parts) > 1 and parts[0].startswith('EAN') else None
        sku = parts[1].split('.')[0] if len(parts) > 1 and parts[1].startswith('SKU') else None
        
        media_type = MediaType.IMAGE
        if filename.endswith('.mp4'):
            media_type = MediaType.VIDEO
        elif filename.endswith('.pdf'):
            media_type = MediaType.DOCUMENT
            
        return cls(
            id=f"{ean}_{sku}_{filename}",
            filename=filename,
            media_type=media_type,
            file_path=file_path,
            ean=ean,
            sku=sku,
            created_at=datetime.now()
        )