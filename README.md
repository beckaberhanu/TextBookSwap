# TextBookSwap

## Django setup

- Consider setting up a virtual environment by using something like pipenv or virtualenv
  - Install python version 3.6 or above
  - https://www.python.org/
- Install version 3 of Django
  - \$ python -m pip install Django
  - https://docs.djangoproject.com/en/3.0/topics/install/
- Install the latest version of Pillow
  - \$ python3 -m pip install --upgrade pip
  - https://pillow.readthedocs.io/en/stable/installation.html
- Install Django crispy forms
  - \$ pip install django-crispy-forms
  - https://django-crispy-forms.readthedocs.io/en/latest/install.html#installing-django-crispy-forms
- You can also optionally use our requirments.in file
  - \$pip install -r requirements.txt
- Clone project from repo

## PostgreSQL setup

- Install Homebrew
  - https://brew.sh/
- Install PostgreSQL
  - \$ brew install postgresql
  - https://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/
- Start PostgreSQL database
  - Open PostgreSQL command line tool
    - \$ psql
  - Create a database called ‘mydb’
    - \# CREATE DATABASE mydb WITH OWNER [insert username here];
- Install the PostgreSQL trigram extension
  - psql
  - Choose the database you want to install the extension for, in this case "mydb"
    - \# \c mydb
  - istall the extension
    - \# CRREATE EXTENSION pg_trgm;
- Install psycopg2
  - \$ pip install psycopg2-binary
  - https://www.psycopg.org/docs/install.html
- Connect the Django project to the PostgreSQL database
  - Export your database username as a local variable
    - \$ export mydb_USER=[insert username here]
  - Export your database password as a local variable
    - \$ export mydb_PASSWORD=[insert password here]
- Delegate an email as the orgnization email
  - Export an email as a local variable
    - \$ export EMAIL_HOST_USER=[insert email here]
  - Export the app password as a local variable
    - \$ export EMAIL_HOST_PASSWORD=[insert app password here]
- Create the necessary migration files
  - \$ python3 manage.py makemigrations
- Perform the migrations
  - \$ python3 manage.py migrate
- Create super user
  - \$ python3 manage.py createsuperuser
  - follow the prompt
- [__OPTIONAL__] create instances
  - run the django shell
    - \$ python3 manage.py shell
  - create randomized user and post instances
    - \ `python from createInstances import reinitialize as re re() \`
  - create real book instances
    - \ `python from createInstances import createRealInstances as cri cri() \`
- Start the server
  - \$ python3 manage.py runserver
