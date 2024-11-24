# Inventory Management System

### NOTES:-

1. To start only need to run api.py file 

2. To create and add new item records go to POST request in POSTMAN with url (http://localhost:8000/items)
and in BODY write like below:

        2.1 For adding 1 item:- 

[
    {
        "item_number": 3,
        "name": "Item 3",
        "description": "Description for Item 3",
        "item_category": "Fashion",
        "price": 10.0,
        "quantity": 50
    }
]


    2.2 For adding mutiple items at once :- (pass each new item record as a spearate element of array in form of dictionary )


[
    {
        "item_number": 1,
        "name": "Item 1",
        "description": "Description for Item 1",
        "item_category": "Category 1",
        "price": 10.0,
        "quantity": 5
    },
    {
        "item_number": 2,
        "name": "Item 2",
        "description": "Description for Item 2",
        "item_category": "Category 2",
        "price": 20.0,
        "quantity": 10
    },
    {
        "item_number": 3,
        "name": "Item 3",
        "description": "Description for Item 3",
        "item_category": "Category 3",
        "price": 30.0,
        "quantity": 15
    }
]

3. For Get Request in POSTMAN use below URL :

    To get all records in inverntory excel : ( http://localhost:8000/items  )

    To get particular item number from inventory excel: ( http://localhost:8000/items/12 )
    (Note: Here 12 is item_number)

4. For Updating existing records use PUT request with url Like ( http://localhost:8000/items/113 )
