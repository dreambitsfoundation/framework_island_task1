# Framework Island - Task 1
## Inventory Management Application.
This is a Django application which implements two models `Inventory` and `Supplier` to cater a CRUD interface to manage suppliers and inventory.

### Main features
1. Supplier CRUD using Django admin interface.
2. Inventory CRUD operation as rendered by entending Django generic View.
3. User Authentication - Only authenticated users can access both the interfaces.

## Installation guidlines
1. Clone this repository into your local system.
2. `cd` into root directory and create a Virtual Environment `python -m venv venv`
3. Activate the virtual environment 
Windows: `venv/Scripts/activate` 
MacOS/Linux: `source venv/bin/activate`
4. Install all dependecies: `pip install -r requirements.txt`
5. Migrate all the models. `python manage.py migrate`
6. Run all the tests `python manage.py test`
7. Create a superuser `python manage.py createsuperuser`
8. Run the development server `python manage.py runserver`

## My local setup
1. OS: Windows 11
2. Python: 3.7.9 (it's fine to use the latest version 3.12.x)

## Play around/User Guide
1. First goto `localhost:8000/admin/`
2. Enter your superuser `username` and `password` to login to Django admin. Now you will be able to access all the pages on the application.
3. Create `Supplier` records by selecting Suppliers option on the left menu.
4. One a new supplier is created, we an click on any existing supplier record to View, Update and Delete that supplier record and also we will be able to Create, View, Update and Delete associated inventories inline on the same page.
5. To access the inventory page we have to goto `localhost:8000/inventory` URL to open the page.
6. We can list all the existing inventory records by supplier name or we can search by name or description of any supplier in the same view.
7. We can edit and delete any inventory using the respective action buttons. 
