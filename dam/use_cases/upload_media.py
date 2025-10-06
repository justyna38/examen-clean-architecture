from typing import List
from dam.entities.media import Media

class UploadMediaUseCase:
    def __init__(self, media_repository, media_storage, product_linker):
        self.media_repository = media_repository
        self.media_storage = media_storage
        self.product_linker = product_linker
    
    def execute(self, file_paths: List[str]) -> List[Media]:
        uploaded_medias = []
        
        for file_path in file_paths:
            filename = file_path.split('/')[-1]
            media = Media.from_filename(filename, file_path)
            
            self.media_storage.store(media)
            self.media_repository.save(media)
            
            if media.ean and media.sku:
                self.product_linker.link_media_to_product(media.ean, media.sku, media.id)
            
            uploaded_medias.append(media)
        
        return uploaded_medias