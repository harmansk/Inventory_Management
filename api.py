# 1. Install required packages and import libraries and configuration

# Import configuration
from config import inventory_file_name, requirements_file

# Install required packages
import install_packages
install_packages.install_packages(requirements_file)

# Import required libraries
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel, field_validator
import logging

# Import functions from load_save_inventory.py
from load_save_inventory import load_inventory_from_excel, save_inventory_to_excel

# 2. Pydantic Model
class Item(BaseModel):
    # record_id: Optional[int] = None
    item_number: int
    name: str
    description: str
    item_category: str
    price: float
    quantity: int

    @field_validator('item_category')
    def item_category_must_not_be_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Item_category must not be blank')
        return v

    @field_validator('name')
    def name_must_not_be_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be blank')
        return v
    
    @field_validator('description')
    def description_must_not_be_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('Description must not be blank')
        return v
    
    @field_validator('item_number')
    def item_number_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Item_number must be a positive integer')
        return v

    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be a positive number')
        return v

    @field_validator('quantity')
    def quantity_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('Quantity must be a non-negative integer')
        return v

# 3. Load existing inventory from Excel

inventory = []
inventory.extend([Item(**item) for item in load_inventory_from_excel(inventory_file_name,output_dataframe=False)])



# 4. API Code
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 4.1 POST - Create a new item
@app.post("/items", response_model=List[Item])
def create_item(items: List[Item]):
    
    # Mutiple items can be created at once
    for item in items:
        for existing_item in inventory:
            # Check if the item_number already exists
            if existing_item.item_number == item.item_number:
                raise HTTPException(status_code=400, detail=f"Item with Item-Number {item.item_number} already exists")
        inventory.append(item)
    save_inventory_to_excel(inventory, inventory_file_name)
    return items

# 4.2 GET - Retrieve records
@app.get("/items", response_model=List[Item])
def get_items():
    return inventory

@app.get("/items/item_number/{item_num}", response_model=Item)
def get_item_by_number(item_num: int):
    for item in inventory:
        if item.item_number == item_num:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items/name/{item_name}", response_model=List[Item])
def get_items_by_name(item_name: str):
    matching_items = [item for item in inventory if item.name.lower() == item_name.lower()]
    if not matching_items:
        raise HTTPException(status_code=404, detail="No items found with the given name")
    return matching_items

@app.get("/items/category/{item_cat}", response_model=List[Item])
def get_items_by_category(item_cat: str):
    matching_items = [item for item in inventory if item.item_category.lower() == item_cat.lower()]
    if not matching_items:
        raise HTTPException(status_code=404, detail="No items found with the given item category")
    return matching_items

@app.get("/items/names", response_model=List[str])
def get_unique_item_names():
    unique_name = list(set(item.name for item in inventory))
    return unique_name

@app.get("/items/categories", response_model=List[str])
def get_unique_item_categories():
    unique_categories = list(set(item.item_category for item in inventory))
    return unique_categories

# 4.3 PUT - Update an item
@app.put("/items/{item_num}", response_model=Item)
def update_item(item_num: int, updated_item: Item):
    for index, item in enumerate(inventory):
        if item.item_number == item_num:
            
            # Check if the item_number is changed and it already exists in another item
            for existing_item in inventory:
                if existing_item.item_number == updated_item.item_number and existing_item.item_number != item.item_number:
                    raise HTTPException(status_code=400, detail="Item with this Item-Number already exists")
            
            inventory[index] = updated_item
            save_inventory_to_excel(inventory, inventory_file_name)
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# 4.4 DELETE - Delete an item
@app.delete("/items/{item_num}", response_model=Item)
def delete_item(item_num: int):
    for index, item in enumerate(inventory):
        if item.item_number == item_num:
            deleted_item = inventory.pop(index)
            save_inventory_to_excel(inventory, inventory_file_name)
            return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
