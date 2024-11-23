# 1. Install required packages and import libraries and configuration

# Install required packages
import install_packages
install_packages.install_packages('requirements.txt')

# Import required libraries
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import logging

# Import configuration
from config import inventory_file_name

# Import functions from load_save_inventory.py
from load_save_inventory import load_inventory_from_excel, save_inventory_to_excel

# 2. Pydantic Model
class Item(BaseModel):
    # record_id: Optional[int] = None
    item_number: int
    name: str
    description: Optional[str] = None
    item_category: str
    price: float
    quantity: int

# 3. Load existing inventory from Excel

inventory = []
inventory.extend([Item(**item) for item in load_inventory_from_excel(inventory_file_name,output_dataframe=False)])



# 2. API Code
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Note: For storing image See imgur / se image hosting service

@app.post("/items", response_model=Item)
def create_item(item: Item):
    
    # Check if the item_number already exists
    for existing_item in inventory:
        if existing_item.item_number == item.item_number:
            raise HTTPException(status_code=400, detail="Item with this Item-Number already exists")
    
    inventory.append(item)
    save_inventory_to_excel(inventory, inventory_file_name)
    return item

@app.get("/items", response_model=List[Item])
def get_items():
    return inventory

@app.get("/items/{item_num}", response_model=Item)
def get_item(item_num: int):
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
def get_items_by_name(item_cat: str):
    matching_items = [item for item in inventory if item.item_category.lower() == item_cat.lower()]
    if not matching_items:
        raise HTTPException(status_code=404, detail="No items found with the given item category")
    return matching_items

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
