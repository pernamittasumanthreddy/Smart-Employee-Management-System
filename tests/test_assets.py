import pytest
from datetime import date
from apps.assets.models import AssetCategory, Asset, AssetStatus

@pytest.mark.django_db
def test_assets():
    cat = AssetCategory.objects.create(name='Laptops')
    asset = Asset.objects.create(asset_id='AST-01', category=cat, name='ThinkPad X1', serial_number='TP-9921', purchase_date=date(2025, 1, 1), status=AssetStatus.AVAILABLE)
    assert asset.status == AssetStatus.AVAILABLE
