from pim.adapters.repositories import InMemoryProductRepository, InMemoryTypologyRepository
from dam.adapters.repositories import InMemoryMediaRepository
from dam.adapters.services import FileSystemMediaStorage, InMemoryProductLinker
from shared.adapters.services import InMemoryEventPublisher
from mdm_core.orchestrator import MDMOrchestrator
from pim.use_cases.create_product import CreateProductUseCase
from dam.use_cases.upload_media import UploadMediaUseCase
from pim.entities.typology import Typology, FieldDefinition

def setup_typologies(typology_repo):
    electronics = Typology(
        name="electronics",
        fields=[
            FieldDefinition("price", "float", True, {}),
            FieldDefinition("processor", "string", True, {}),
            FieldDefinition("ram", "string", False, {})
        ]
    )
    
    textile = Typology(
        name="textile",
        fields=[
            FieldDefinition("price", "float", True, {}),
            FieldDefinition("size", "string", True, {}),
            FieldDefinition("color", "string", True, {}),
            FieldDefinition("material", "string", False, {})
        ]
    )
    
    typology_repo.save(electronics)
    typology_repo.save(textile)

def main():
    product_repo = InMemoryProductRepository()
    typology_repo = InMemoryTypologyRepository()
    media_repo = InMemoryMediaRepository()
    media_storage = FileSystemMediaStorage("./storage")
    product_linker = InMemoryProductLinker()
    event_publisher = InMemoryEventPublisher()
    
    setup_typologies(typology_repo)
    
    orchestrator = MDMOrchestrator(event_publisher, product_repo, media_repo)
    
    create_product_use_case = CreateProductUseCase(product_repo, typology_repo)
    upload_media_use_case = UploadMediaUseCase(media_repo, media_storage, product_linker)
    
    product = create_product_use_case.execute(
        ean="EAN12345",
        name="Gaming Laptop",
        typology_name="electronics",
        attributes={"price": 1299.99, "processor": "Intel i7", "ram": "16GB"}
    )
    
    print(f"Created product: {product.name} (EAN: {product.ean})")
    
    medias = upload_media_use_case.execute([
        "/path/to/EAN12345_SKU56789_front.jpg",
        "/path/to/EAN12345_SKU56789_back.jpg"
    ])
    
    print(f"Uploaded {len(medias)} media files")
    for media in medias:
        print(f"  - {media.filename} (EAN: {media.ean}, SKU: {media.sku})")

if __name__ == "__main__":
    main()