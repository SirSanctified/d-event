# D-Event

D-Event is a simple full-stack web application for event registration and management. It is built using the Django framework and provides an intuitive user-interface for users
to view and search for events, register for them and unregister if needed.
It also provides admin and moderator dashboards for managing events.

## Features

The main features of the application include:

- ### Participant Dashboard

  ![](/static/images/d-event-participant-dashboard.png)
  - View all events
  - Search for events
  - Register for events
  - Unregister from events
  - View registered events
  - View event details
  
- ### Speaker Dashboard
  
  ![](/static/images/d-event-speaker-dashboard.png)
  
  - View all events
  - Search for events
  - View events they are presenting
  - View event details
  
- ### Moderator Dashboard
  
  ![](/static/images/d-event-mod-dashboard.png)

  - View all events
  - Add new events
  - Edit events
  - Delete events
  - View event details
  - Search for events
  - Add event categories
  - Edit event categories
  - Delete event categories
  - View participants
  - View speakers
  - View all messages from users
  - Delete messages
  
- ### Admin Dashboard

  ![](/static/images/d-event-admin-dashboard.png)
  
  - View all events
  - Add new events
  - Edit events
  - Delete events
  - View event details
  - Search for events
  - Add event categories
  - Edit event categories
  - Delete event categories
  - View participants
  - Edit participants
  - Delete participants
  - View speakers
  - Edit speakers
  - Delete speakers
  - View all messages from users
  - Delete messages
  - View all users
  - Edit users
  - Delete users
  - Create user groups
  - Add users to groups
  - etc

- ### User Authentication
  
  ![](/static/images/d-event-login.png)
  
  - Login
  - Logout
  - Register
  - Reset password
  - Change password
  - Update profile
  - Delete profile

## Installation and Usage

1. Clone the repository

   ```bash
   $ git clone https://github.com/SirSanctified/d-event.git
    ```

2. Set up the database
   - Create a new database in MySQL
   - Create a new user and give it permissions to access the database

3. Create and activate virtual environment for the project

   ```bash
   $ virtualvenv venv
   $ source venv/bin/activate
   ```
   
4. Install project dependencies
  
    ```bash
    $ pip install -r requirements.txt
    ```

5. Run database migrations

    ```bash
    $ python manage.py migrate
    ```
6. Create superuser to access the admin dashboard

    ```bash
    $ python manage.py createsuperuser
    ```
7. Run the development server

    ```bash
   $ python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000`


Once the application is running, you can then add events from the admin/moderator dashboard,
search for events and register for them.

## Authors

D-Event is developed and maintained by [Pritchard Mambambo](https://pritchardmambambo.tech)

## Support and Contact

- [Twitter](https://twitter.com/Sir_sanctified)
- [LinkedIn](https://linkedin.com/in/pritchard-mambambo-611427193)
