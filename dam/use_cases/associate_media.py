class AssociateMediaUseCase:
    def __init__(self, media_repository, product_linker):
        self.media_repository = media_repository
        self.product_linker = product_linker
    
    def execute(self, media_id: str, ean: str, sku: str) -> None:
        media = self.media_repository.get_by_id(media_id)
        if not media:
            raise ValueError(f"Media with ID {media_id} not found")
        
        media.ean = ean
        media.sku = sku
        self.media_repository.save(media)
        
        self.product_linker.link_media_to_product(ean, sku, media_id)