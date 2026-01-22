# Lesson 25: Deploying the Website

Now that we have completed our todo list website and mobile app, it is time to deploy them. We will start by deploying the website. Before you begin, make sure that the development server and mobile app are not running. Our website can be either self-hosted or hosted on a cloud hosting platform. For this tutorial I will be using Supabase to host the database and Vercel to host the Django project. As of the time this tutorial was last updated, both provide a free tier for hobbyist projects. The first thing we need to do is visit https://supabase.com/ and goto the dashboard page. If you don't already have an account, you will need to create one. Next you will need to create an organization. You can name it whatever you want, but be sure to set the type to Personal and the plan to Free. Then you can create a new project. I will be naming mine "Simple Todo DB". You can choose to enter a password or have one generated. If you choose to generate one, be sure to copy it and paste it into a text file to use later. Under the security options set the connection type to Only Connection String. After you create your new Supabase project you will need to wait a bit for it to startup. Once the project is started, visit the project homepage and scroll down to the Connect button. Click the Connect button and copy the connection string. Then paste the connection string into a text file and replace `[YOUR-PASSWORD]` with the password for your Supabase project.

Next we need to rename `simple-todo/simple_todo/.env` to `.env.dbg`. Then copy `simple-todo/simple_todo/.env.dist` and name it `.env`. Open `simple-todo/simple_todo/.env`, generate a new secret key, and set the database URL to the Supabase connection string. Open `simple-todo/requirements.txt` and modify it like this:
```
Django
django-allauth
django-environ
django-htmx
djangorestframework
djangorestframework-simplejwt
httpx
kivy
psycopg
```

Now open a new terminal in Visual Studio Code and execute the following command to install the additional dependencies:
```sh
pip install -r requirements.txt
```

Next, execute the following commands to apply migrations to the production database:
```sh
cd simple_todo
python manage.py migrate
```

Now open `simple-todo/simple_todo/simple_todo/settings.py` and set the allowed hosts like this:
```python
ALLOWED_HOSTS = [] if DEBUG else [
    ".vercel.app",
    ".now.sh"
]
```

Then add the static root setting below the static URL setting. It should be set to the directory to collect your static files into in order to serve them. For example, you can configure your static root to be `simple-todo/simple_todo/static/` like this:
```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
```

Next, add the following section to your settings. This will prevent sending CSRF and session cookies over HTTP in a production environment:
```python
# Cookie security
CSRF_COOKIE_SECURE = not env("DEBUG")
SESSION_COOKIE_SECURE = not env("DEBUG")
```

If your website needs to send email, you will need to configure the email settings as well. You can also set the admins setting to a list of email addresses which should receive an email whenever a 500 error occurs. However, I will not be covering these topics in this tutorial. Next we need to add the CSP middleware to our list of middleware:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware"
]
```

We also need to add the following section to configure a content security policy. This will prevent our website from loading resources from hosts other than the one our website is served from:
```python
# Content security policy
from django.utils.csp import CSP

CSP_SECURE = {
    "default-src": [CSP.SELF]
}
```

Now we need to create `simple-todo/simple_todo/requirements.txt` with the following content:
```
Django
django-allauth
django-environ
django-htmx
djangorestframework
djangorestframework-simplejwt
psycopg
```

This file will determine what dependencies need to be installed by Vercel in order to run our website. Next we need to create `simple-todo/simple_todo/build-files.sh` with the following content:
```sh
# build-files.sh
pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput
```

This script will be run to build our website. We also need to create `simple-todo/simple_todo/vercel.json` with the following content:
```json
{
    "version": 2,
    "builds": [
        {
            "src": "simple_todo/wsgi.py",
            "use": "@vercel/python",
            "config": {
                "maxLambdaSize": "15mb"
            }
        },
        {
            "src": "build_files.sh",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "static"
            }
        }
    ],
    "routes": [
        {
            "src": "/static/(.*)",
            "dest": "/static/$1"
        },
        {
            "src": "/(.*)",
            "dest": "simple_todo/wsgi.py"
        }
    ]
}
```

If you haven't already, you will need to create a GitHub repository for your project and push all your code to it. Make sure you choose python for your .gitignore template and that `simple-todo/simple_todo/.env.dbg` and `simple-todo/simple_todo/.env.prod` are added to your `.gitignore` file.

Next, visit https://vercel.com/ and goto the dashboard page. Click Add New... > Project. You will need to link your GitHub account to your Vercel account the first time you do this. You will also need to install the Vercel GitHub app into your GitHub account and choose which repos it will have access to. Then choose to import the GitHub repo for your todo list website. On the next page, expand the Environment Variables section and import your .env file. Click the Deploy button and wait for the deployment to complete.
