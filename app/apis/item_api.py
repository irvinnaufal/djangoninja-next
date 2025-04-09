from ninja import Router
from ..schemas.item_schema import ItemSchema
from ..services.item_service import get_paginated_items, create_item, update_item, delete_item

item_api = Router()

# List items (only active ones)
@item_api.get("/", response=dict, by_alias=True, tags=["Items"])
def list_items_view(request, page: int = 1, page_size: int = 10):
    return get_paginated_items(page, page_size)

# Create item
@item_api.post("/", response=ItemSchema)
def create_item_view(request, item: ItemSchema):
    return create_item(item.dict(exclude_unset=True))

# Update item
@item_api.put("/{item_id}", response=ItemSchema | dict)
def update_item_view(request, item_id: int, item: ItemSchema):
    data = item.dict(exclude_unset=True)
    # ✅ Remove 'id' from the incoming data to prevent overwriting
    data.pop("id", None)  
    updated_item = update_item(item_id, data)
    if not updated_item:
        return {"error": "Item not found"}  # Proper error response
    return updated_item  # Return updated item

# Soft delete item (set is_active to False)
@item_api.delete("/{item_id}", response=dict)
def delete_item_view(request, item_id: int): 
    success = delete_item(item_id)
    return {"success": success, "message": "Item deleted"} if success else {"error": "Item not found"}
