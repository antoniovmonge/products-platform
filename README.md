# Products Platform

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

🚧 Under construction. Work in Progress 🚧

## 👨‍🏫 App Description

This platform allows users to **compare products** analyzing their **environmental impact**. 📊 🌱

It also allows manufacturers to upload their Products with all the info and certificates.

## Stack

- Python 🐍
- Django
- **HTMX** (The new super Star) ⭐
- Docker 🐳
- HTML/CSS
- Celery
- Redis

## 🚀 Get the app and launch it in your computer

⚠ At this stage, due to ownership of the data,it is needed an extra CSV that could be requested to load and test the application. **The data are not uploaded to the repository** (.gitignore).

### 1. Download/Clone the code

```bash
gh repo clone antoniovmonge/products-platform
```

### 2. Build the image

Once the code is in your computer (and you are in the directory), run the following command:

```bash
docker-compose -f local.yml up --build
```

❕ My suggestion is to write this command in a terminal that remains open. In this way it is possible to check what is going on, (or if something goes wrong).

### 3. What happened so far

When the application runs locally, it also loads the following data to the db to allow testing everything faster without needing to create products and users manually.

What has been created so far:

Users:

- a **superuser**
- a normal **user**
- a user that is **company-admin**. This user has CRUD permissions for the products of the company it belongs.

Products and Companies:

- Also the csv of lo load the products and companies is required, but to the date it is not included due to data ownership. This file can be requested to me for running a demo. (In the future there will be some test/fake data included to run a demo directly.)

The commands are on the path `compose/local/django/start`

To know the email and password of the automatically created users, please check the code that generates them under the path `pplatform/users/management/commands`:

- **superuser** and "basic" **user**: `create_local_user_and_admin.py`
- **company-admin user**: `create_local_company_admin.py`

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

```bash
python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

```bash
mypy pplatform
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

#### Running tests with pytest

```bash
pytest
```

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd pplatform
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
