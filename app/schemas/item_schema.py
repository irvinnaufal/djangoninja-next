# api/schemas/item_schema.py
from ninja import ModelSchema
from ..models.item import Item

class ItemSchema(ModelSchema):
    class Config:
        model = Item
        model_fields = ['id', 'name', 'description']
