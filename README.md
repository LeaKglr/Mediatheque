# Mediatheque

The media library is made up of 2 applications: librarians and borrowers. Librarians can consult and borrow books, 
CDs and DVDs. Borrowers can only view the media list.
This project was generated with [Django] version 5.1.3

# Create a virtual environment
A virtual environment will allow you to create a separate space for each project, thus making it possible to isolate 
the packages used from other projects that you may have.

Example for create environment, use this command :
python -m venv nameFile-env

Then, to activate this environment and place yourself in it :

cd nameFile-env

cd nameProject

cd Scripts

activate

cd ../

# Installation django
To install django in the project :

python -m pip install Django

# Development server

To deploy this project use the terminal and write :

python manage.py runserver

Navigate to 'http://127.0.0.1:8000/'. The application will automatically reload if you change any of the source files.

# Running Tests
To run tests, go in to the terminal and write :

python manage.py test bibliothecaire

or

python manage.py test membre
