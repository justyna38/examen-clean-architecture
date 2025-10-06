import pytest
from unittest.mock import Mock
from dam.use_cases.upload_media import UploadMediaUseCase

class TestUploadMediaUseCase:
    def test_upload_media_with_ean_sku(self):
        mock_media_repo = Mock()
        mock_media_storage = Mock()
        mock_product_linker = Mock()
        
        use_case = UploadMediaUseCase(mock_media_repo, mock_media_storage, mock_product_linker)
        
        result = use_case.execute(["/path/to/EAN12345_SKU56789_front.jpg"])
        
        assert len(result) == 1
        assert result[0].ean == "EAN12345"
        assert result[0].sku == "SKU56789"
        mock_media_storage.store.assert_called_once()
        mock_media_repo.save.assert_called_once()
        mock_product_linker.link_media_to_product.assert_called_once_with("EAN12345", "SKU56789", result[0].id)
    
    def test_upload_media_without_ean_sku(self):
        mock_media_repo = Mock()
        mock_media_storage = Mock()
        mock_product_linker = Mock()
        
        use_case = UploadMediaUseCase(mock_media_repo, mock_media_storage, mock_product_linker)
        
        result = use_case.execute(["/path/to/regular_file.jpg"])
        
        assert len(result) == 1
        assert result[0].ean is None
        assert result[0].sku is None
        mock_product_linker.link_media_to_product.assert_not_called()
    
    def test_upload_media_storage_error(self):
        mock_media_repo = Mock()
        mock_media_storage = Mock()
        mock_media_storage.store.side_effect = Exception("Storage full")
        mock_product_linker = Mock()
        
        use_case = UploadMediaUseCase(mock_media_repo, mock_media_storage, mock_product_linker)
        
        with pytest.raises(Exception, match="Storage full"):
            use_case.execute(["/path/to/EAN12345_SKU56789_front.jpg"])
    
    def test_upload_media_invalid_filename_format(self):
        mock_media_repo = Mock()
        mock_media_storage = Mock()
        mock_product_linker = Mock()
        
        use_case = UploadMediaUseCase(mock_media_repo, mock_media_storage, mock_product_linker)
        
        result = use_case.execute(["/path/to/invalid_filename.jpg"])
        
        assert len(result) == 1
        assert result[0].ean is None
        assert result[0].sku is None
        mock_product_linker.link_media_to_product.assert_not_called()