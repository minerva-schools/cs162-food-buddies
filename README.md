# Foodbuddies

#### Foodbuddies is a web application for Minervans to find a meal companion - a Foodbuddy! The web app has the following main pages, each a corresponding .css file of the same name:
* login.html - a Login page that asks the user for their email and password, authentication is run in the back-end to determine if the user input does correspond to an existing user stored in the DB, and either load the Preferences page, warn that the user does not exist, or the user can choose to sign up;
resetPassword.html - to reset their password;
* signUp.html - a sign up page where the user has to input a Minerva email (@minerva.kgi.edu), their current Rotation city, a chosen password and repeat it, and their preferred method of contact since the app does not have a chat function, and it is up to the user to reach out to the Foodbuddies we match them with;
* preference.html - where the user can select their dietary restrictions, the meal (breakfast, lunch, or dinner), the cuisine, and can input a window of availability for the meal;
* matches.html the matching page where the user is presented with matches that could potentially be their Foodbuddies. The user can see each match, their meal preferences, and their preferred method of contact so that they can contact them to coordinate. There are three main layers to the matching process: first we match on all preferences of the user, if this strict matching doesn’t yield a match, we omit dietary restrictions in the matching, if this yields nothing as well, then we yield cuisine as well;
* followup.html - a follow up survey page where we ask the user to provide us with details of what happened after the matching page (did they contact a match, were they contacted, how, how accurate was the matching, etc.). At the end, the user can choose to go back to the preferences pages or log out;
* 404.html - the error page for requesting an invalid page or no access to the requested page.
* A pop-up to input the email in case the user forgot their password;
* A page where the user can edit their password;
* A pop-up for the user to edit their user information.


#### This version of the Foodbuddies web app has the following notable features:
* The Sign Up page checks if the email is a Minerva email (@minerva.kgi.edu), if the passwords match, and if they fulfill the minimal password requirements;
* We display a user profile picture that can be edited and supports a .png file;
* The Matching page was designed with flexibility in mind, so that the user could still change their preferences an watch their matches changes;




## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

## Deployment with Heroku
We deployed the app with Heroku for most of the development phase since it was more convenient than using Docker:
https://foodbuddies-cs162.herokuapp.com/


## Environment Variables

All environment variables are stored within the `.env` file and loaded with dotenv package.


## Run the Application
    $ python -m venv venv
    $ source venv/bin/activate
    # Activate virtual environment for MAC/UNIX
    $ venv\Scripts\activate
    # Activate virtual environment for WINDOWS
    $ pip install -r requirements.txt
    $ export FLASK_ENV=development
    $ export FLASK_CONFIG=dev
    $ export FLASK_APP=web
    $ python3 -m flask run


## Unit Tests
To run the unit tests use the following commands:

    $ python3 -m venv venv_unit
    $ source venv_unit/bin/activate
    # Activate the virtual environment for MAC/UNIX
    $ venv_unit\Scripts\activate
    # Activate virtual environment for WINDOWS
    $ pip install -r requirements-unit.txt
    $ export TEST_SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    $ export FLASK_CONFIG=test
    $ python3 -m pytest unit_test


## Integration Tests
We used Travis CI to run continuous integration tests as we merged and added code in the Github repo.


Now run the integration tests using the following commands:

    $ python3 -m venv venv_integration
    $ source venv_integration/bin/actvate
    $ pip3 install -r requirements-integration.txt
    $ pytest integration_test
