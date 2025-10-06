import pytest
from unittest.mock import Mock
from pim.entities.typology import Typology, FieldDefinition
from pim.use_cases.create_product import CreateProductUseCase

class TestCreateProductUseCase:
    def test_create_product_success(self):
        typology = Typology(
            name="electronics",
            fields=[
                FieldDefinition("price", "float", True, {}),
                FieldDefinition("processor", "string", True, {}),
                FieldDefinition("ram", "string", False, {})
            ]
        )
        
        mock_product_repo = Mock()
        mock_typology_repo = Mock()
        mock_typology_repo.get_by_name.return_value = typology
        mock_product_repo.save.return_value = Mock()
        
        use_case = CreateProductUseCase(mock_product_repo, mock_typology_repo)
        
        result = use_case.execute(
            ean="123456789",
            name="Laptop",
            typology_name="electronics",
            attributes={"price": 999.99, "processor": "Intel i7"}
        )
        
        mock_typology_repo.get_by_name.assert_called_once_with("electronics")
        mock_product_repo.save.assert_called_once()
        assert result is not None
    
    def test_create_product_missing_required_field(self):
        typology = Typology(
            name="electronics",
            fields=[
                FieldDefinition("price", "float", True, {}),
                FieldDefinition("processor", "string", True, {})
            ]
        )
        
        mock_product_repo = Mock()
        mock_typology_repo = Mock()
        mock_typology_repo.get_by_name.return_value = typology
        
        use_case = CreateProductUseCase(mock_product_repo, mock_typology_repo)
        
        with pytest.raises(ValueError, match="Required field processor is missing"):
            use_case.execute(
                ean="123456789",
                name="Laptop",
                typology_name="electronics",
                attributes={"price": 999.99}
            )
    
    def test_create_product_invalid_typology(self):
        mock_product_repo = Mock()
        mock_typology_repo = Mock()
        mock_typology_repo.get_by_name.return_value = None
        
        use_case = CreateProductUseCase(mock_product_repo, mock_typology_repo)
        
        with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'fields'"):
            use_case.execute(
                ean="123456789",
                name="Laptop",
                typology_name="nonexistent",
                attributes={"price": 999.99, "processor": "Intel i7"}
            )
    
    def test_create_product_invalid_ean_format(self):
        typology = Typology(
            name="electronics",
            fields=[
                FieldDefinition("price", "float", True, {}),
                FieldDefinition("processor", "string", True, {})
            ]
        )
        
        mock_product_repo = Mock()
        mock_typology_repo = Mock()
        mock_typology_repo.get_by_name.return_value = typology
        
        use_case = CreateProductUseCase(mock_product_repo, mock_typology_repo)
        
        with pytest.raises(ValueError, match="EAN must be at least 8 characters"):
            use_case.execute(
                ean="123",  # EAN trop court
                name="Laptop",
                typology_name="electronics",
                attributes={"price": 999.99, "processor": "Intel i7"}
            )