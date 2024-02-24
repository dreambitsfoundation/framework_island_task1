# Framework Island - Task 1

## Inventory Management Application.

This is a Django application which implements two models `Inventory` and `Supplier` to cater a CRUD interface to manage suppliers and inventory.

### Main objectives

1. Supplier CRUD using Django admin interface.
2. Inventory CRUD operation as rendered by entending Django generic View.
3. User Authentication - Only authenticated users can access both the interfaces.

### Design

#### Requirement Analysis

As per the requirement

1. Facilitate CRUD operations for Supplier model using Django Admin interface.
2. Facilitate CRUD operations for Inventory model using Django Generic View.
3. Search inventories on the Inventory page by name or description.

Note: Unit tests will be added for each Model, Form and View.

#### Consideations

Following are the considerations that I have made before beginning the development:

1. Generally this is ideal to have `super admin` to create a `Supplier` profile and a supplier user who can
   further create `Inventory` records associated with it. But since this is not mentioned
   explicitely in the requirment to give a focus towards it, I am considering `super admin`
   is making CRUD operations in both `Supplier` and `Inventory` table. And hence enabling
   both the the services under same login.
2. In the Inventory UI I am keeping both search by name/description along with filter by supplier.
   I am keeping the forms to reduce JS code involvement and ease of understanding.

#### Database Design

1. In this project `Supplier` table has been employed as the parent table.
2. Then there is `Inventory` table which represents the Products.
3. Inventory table has a foreignkey relation with the Supplier through the `supplier_id` field.

#### Application

** Program Setup **

1. We'll be registering both `Supplier` and `Inventory` table in the Django Admin
2. Initial use of Django Admin will be to create Supplier records and Create/Modify
   associated Inventory records inline on the Django Admin. No special customisation will be
   done to `Inventory` model for Django Admin.
3. We'll be extending the Django generic view module to implement all GET, POST, UPDATE and DELETE
   funtionality over Inventory model.

** User Authentication and View security decissions **

1. As decided in the pre-development considerations, this view will be protected by
   autentication logic.
2. Any un-aunthenticated user should be redirected to the Django admin login page while trying to access
   any of the pages
3. Further since there is an API implementation required for DELETE operation, we'll be exempting
   CSRF token requirement on the inventory view.

** Cosmetic features **

1. The Inventory page will be supplied with 2 inventory search options `Search by Name/Description` and `Search by Supplier`.
   Both of these searches will be handled by the GET view.
2. Individual Inventory search results will offer an option to Edit and Delete the record,
   which will be handled by the inventory view itself.

** Storage **

1. Since the requirement is very straight forward, we'll be using SQlite file database storage.
2. All the image files associated with the inventory form will be saved in the defined directory within the project.

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


# Framework Island - Task 3

## Inventory Management Application Report Generation Dashboard.

This is an extension of Django application for Inventory Management.

### Main objectives

1. Design an API interface which returns all the fields for Inventory and Supplier Model
2. Design a query interface which allow filter, sorting and output field selection for report.
3. Develop and endpoint to make the report downloadable.

### Design

#### Requirement Analysis

As per the requirement

1. Facilitate CRUD operations for Supplier model using Django Admin interface.
2. Facilitate CRUD operations for Inventory model using Django Generic View.
3. Search inventories on the Inventory page by name or description.
4. Cache the query results on the go to make forthcoming queries less expensive.

#### Consideations

Following are the considerations that I have made before beginning the development:

1. There will be API implementation with DRF to cater field options, filter options, sorting options and result field selection. Plan is to build 3 different REST API endpoints.
2. Result can be exported within 30 minutes of the query, else the query will be deleted from cache. I am doing this to avoid making duplicate queries for a generated report.
3. A UI has to be implemented for field selection and result rendering.

#### Application

** Program Setup **

1. We'll be creating a new application to handle all Rest APIs.
2. We'll keep two seperate views:
   - Field choice and value option
   - Querying and file download.


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
8. Create a directory named `export_files` inside the root directory.
9. Run the development server `python manage.py runserver`

## My local setup

1. OS: Windows 11
2. Python: 3.7.9 (it's fine to use the latest version 3.12.x)

## Play around/User Guide

1. Goto `localhost:8000/api/filter_fields` *method: GET* to see all field names and options per model.

   Sample Response
   ```json
   [
      {
         "model_name": "Supplier",
         "field_data": [
               {
                  "visible_name": "name",
                  "model_name": "Supplier",
                  "filter_name": "supplier__name",
                  "numeric_field": false,
                  "possible_options": [
                     "Supplier 1",
                     "Supplier 2"
                  ]
               }
         ]
      },
      {
         "model_name": "Inventory",
         "field_data": [
               {
                  "visible_name": "name",
                  "model_name": "Inventory",
                  "filter_name": "name",
                  "numeric_field": false,
                  "possible_options": [
                     "inv_s1_test",
                     "inv2_s1_test2"
                  ]
               },
               {
                  "visible_name": "quantity_in_stock",
                  "model_name": "Inventory",
                  "filter_name": "quantity_in_stock",
                  "numeric_field": true,
                  "possible_options": [
                     20,
                     100
                  ]
               },
               {
                  "visible_name": "price",
                  "model_name": "Inventory",
                  "filter_name": "price",
                  "numeric_field": true,
                  "possible_options": [
                     30.0,
                     200.0
                  ]
               }
         ]
      }
   ]
   ```

2. To make a query use the API `localhost:8000/api/filter_query` *method: POST* to make a query.

   Sample Request
   ```json
   {
      "fields": ["name", "sku", "quantity_in_stock", "supplier__name", "supplier__address"],
      "filter": [
         {"field": "supplier__name", "value": "Supplier 1"},
         {"field": "quantity_in_stock", "operator": "gte", "value": 20}
      ],
      "sorting": {"field": "quantity_in_stock", "order": "asc"}
   }
   ```
   Following is a list of filters
   ```json
   {
      "filter": [
        {
            "field": "<field_name>",
            "operation": "gt | lt | gte | lte"
            "value": "<value>"
        }
      ],
      "sorting": {
         "field": "<field_name>",
         "order": "asc|dsc"
      },
      "fields": []
   }
   ```
   Sample API Response
   ```json
   {
      "download_url": "/api/download_file/<download_token>",
      "data": [
         {
               "name": "inv_s1_test",
               "sku": "a3603c27-c863-4050-a0d5-9af7f7bc86eb",
               "quantity_in_stock": 20,
               "supplier": {
                  "name": "Supplier 1",
                  "address": "some information"
               }
         },
         {
               "name": "inv2_s1_test2",
               "sku": "cc099305-b674-407b-abdd-b5f27e45328f",
               "quantity_in_stock": 100,
               "supplier": {
                  "name": "Supplier 2",
                  "address": "some information"
               }
         }
      ]
   }
   ```

3. To Download report file use `localhost:8000/api/download_file/<download_token>` *method: GET*
   Note: You will get the *download_token* in the response of Section 2.
