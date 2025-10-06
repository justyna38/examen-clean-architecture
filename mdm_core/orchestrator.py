from mdm_core.interfaces.services import IEventPublisher
from pim.interfaces.repositories import IProductRepository
from dam.interfaces.repositories import IMediaRepository

class MDMOrchestrator:
    def __init__(self, event_publisher: IEventPublisher, 
                 product_repository: IProductRepository,
                 media_repository: IMediaRepository):
        self.event_publisher = event_publisher
        self.product_repository = product_repository
        self.media_repository = media_repository
    
    def handle_media_uploaded(self, ean: str, sku: str, media_id: str) -> None:
        product = self.product_repository.get_by_ean(ean)
        if product:
            self.event_publisher.publish("product_media_linked", {
                "ean": ean,
                "sku": sku,
                "media_id": media_id,
                "product_name": product.name
            })
    
    def validate_ean_sku(self, ean: str, sku: str) -> bool:
        if not ean or not sku:
            return False
        if len(ean) < 8 or len(sku) < 3:
            return False
        return True