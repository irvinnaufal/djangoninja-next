from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from ..models.item import Item
from ..schemas.item_schema import ItemSchema
from ..utils.response import success_response, error_response
from ..utils.logging import handle_service_call  # ✅ Import logging utility

# ✅ Get paginated items
@handle_service_call
def get_paginated_items(page: int = 1, page_size: int = 10):
    queryset = Item.objects.filter(is_active=True).order_by("id")
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    return success_response({
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "next": page + 1 if page_obj.has_next() else None,
        "previous": page - 1 if page_obj.has_previous() else None,
        "results": [ItemSchema.from_orm(item).dict() for item in page_obj.object_list],
    }, "Items fetched successfully")

# ✅ Create a new item
@handle_service_call
def create_item(data):
    item = Item.objects.create(**data)
    return success_response(ItemSchema.from_orm(item).dict(), "Item created successfully", 201)

# ✅ Update an item
@handle_service_call
def update_item(item_id, data):
    item = get_object_or_404(Item, id=item_id, is_active=True)
    for key, value in data.items():
        setattr(item, key, value)
    item.save()
    return success_response(ItemSchema.from_orm(item).dict(), "Item updated successfully")

# ✅ Soft delete an item
@handle_service_call
def delete_item(item_id):
    updated_count = Item.objects.filter(id=item_id, is_active=True).update(is_active=False)

    if updated_count == 0:
        return error_response("Item not found or already deleted", 404)

    return success_response(message="Item deleted successfully")
