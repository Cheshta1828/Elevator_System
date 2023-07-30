------------------------------------------------------**Elevator Control System API**------------------------------------------------------------------------

This is a Django-based Elevator Control System API that allows you to manage buildings and their associated elevators.
The API provides endpoints to create, update, view, and delete buildings and elevators. 
Additionally, it allows users to request elevators from both inside and outside the buildings.

--------------------------------------------------------**Architecture**--------------------------------------------------------------------------------------

The project is built using Django, a popular web framework in Python. The architecture follows a standard Model-View-Controller (MVC) pattern. It uses Django Rest Framework (DRF) to create RESTful APIs for building and elevator management.

The project uses a threaded approach to manage multiple elevator instances efficiently. Each elevator is controlled by a separate thread, allowing them to run concurrently and handle requests efficiently.

--------------------------------------------------------**Repository Structure**------------------------------------------------------------------------------

The project has the following main components:

elevatorapp: This app contains the models, views, and serializers for handling buildings, elevators, and elevator requests.
elevatorapp/constants.py: This file contains the definition of RunningStatus enum for elevator status.
elevatorapp/logic.py: This file contains the implementation of the ElevatorController, which controls the behavior of individual elevators in a separate thread.
elevatorapp/serializers.py: This file contains the serializers for building, elevator, and elevator request models.
elevatorapp/utils.py: This file contains utility functions for calculating floor distances for elevator requests.
elevatorapp/views.py: This file contains the API views for building, elevator, and elevator request endpoints.
elevatorcontrol: This is the main Django project folder that contains settings, URLs, and other configurations.

-------------------------------------------------------**Database Modeling**---------------------------------------------------------------------------------

The project uses Django's built-in ORM to manage the database. There are three main models:

Building: Represents a building with elevators. It has a one-to-many relationship with Elevator.
Elevator: Represents an elevator associated with a building. It contains attributes for elevator status and position.
ElevatorRequest: Represents a request made to an elevator from both inside and outside the building.

-----------------------------------------------------------**API Contracts**-----------------------------------------------------------------------------

The API provides the following endpoints:

POST /buildings/: Create a new building.
GET /buildings/: List all buildings.
GET /buildings/<building_id>/: Retrieve details of a specific building.
PUT /buildings/<building_id>/: Update details of a specific building.
DELETE /buildings/<building_id>/: Delete a specific building.
POST /elevator/: Create a new elevator for a building.
GET /elevator/: List all elevators.
GET /elevator/<elevator_id>/: Retrieve details of a specific elevator.
PUT /elevator/<elevator_id>/: Update details of a specific elevator.
DELETE /elevator/<elevator_id>/: Delete a specific elevator.
POST /request_outside_elevator/: Request an elevator from outside the building. (Supply building_id and destination_floor in the request body)
POST /request_inside_elevator/: Request an elevator from inside the building. (Supply elevator_id, building_id, and destination_floor in the request body)
POST /elevator_status/: Get the status of a specific elevator. (Supply elevator_id in the request body)

-------------------------------------------------------------------**Setup, Deploy, and Test**------------------------------------------------------------

Clone the repository: git clone https://github.com/Cheshta1828/Elevator_System
Install the required dependencies: cd elevator-control-system
pip install -r requirements.txt
Apply database migrations: python manage.py migrate
Create a superuser for admin access: python manage.py createsuperuser
Run the development server: python manage.py runserver
---------------------------------------------------------------------**Documentation**--------------------------------------------------------------

Access the API in your browser at http://localhost:8000/<endpoint>/ or the admin panel at http://localhost:8000/admin/.
Access the Swagger documentation at http://localhost:8000/api/schema/docs/.

Use tools like curl, Postman, or write test cases using Django's built-in TestCase to test the API endpoints.

-------------------------------------------------------------------**Libraries and Plugins**-----------------------------------------------------

The project uses the following main libraries and plugins:

Django: Web framework for building the API.
Django Rest Framework (DRF): To create RESTful APIs.
drf-spectacular: For API schema generation and documentation.

-------------------------------------------------------------------**Conclusion**---------------------------------------------------------------

This Elevator Control System API provides a simple and efficient way to manage buildings, elevators, and elevator requests. It follows a threaded approach to handle multiple elevator instances concurrently, providing real-time elevator management. Feel free to explore the API and use it as a base for your elevator control system. If you have any questions or need further assistance, please feel free to contact the project maintainers.

