# Inventory Management System

### NOTES:-

1. To start only need to run api.py file 

2. To create and add new item records go to POST request in POSTMAN with url (http://localhost:8000/items)
and in BODY write like below:
{
    "item_number" : 112,
    "name": "Laptopn I3 ",
    "description": "Mid Spec Laptop",
    "item_category": "Electronics",
    "price": 590.9,
    "quantity": 22
}

3. FOr Get Request in POSTMAN use below URL :

To get all records in inverntory excel : ( http://localhost:8000/items  )

To get particular item number from inventory excel: ( http://localhost:8000/items/12 )
(Note: Here 12 is item_number)

4. For Updating existing records use PUT request with url Like ( http://localhost:8000/items/113 )
