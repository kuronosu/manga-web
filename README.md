# MangaWeb

### Installing:

1. Clone the repository
```
$ git clone https://github.com/kuronosu/manga-web.git
cd manga-web
```
2. Create a virtualenv and install the dependencies for python and node
```
$ virtualenv venv
$ ./venv/bin/activate # Linux
$ ./venv/Scripts/activate # Windows
$ pip install -r requirements.txt
$ cd ./frontend
$ npm install # or yarn add
```
3. Create local settings files for django in ./backend/configuration

**environmentVariables.py**
```
import os

os.environ['SECRET_KEY'] = 'your secret key'
os.environ['EMAIL_PORT'] = '25'
os.environ['EMAIL_HOST_USER'] = 'your mail'
os.environ['EMAIL_HOST_PASSWORD'] = 'your mail password'
os.environ['DBUSER'] = 'your database user'
os.environ['DBNAME'] = 'your database name'
os.environ['DBPASS'] = 'your database password'
```
**localSettings.py**
```
DEBUG = True
```
**localUrls.py**
```
from django.urls import path
from django.contrib import admin

LOCAL_URLS = [
    path('admin/', admin.site.urls),
]
```
4. Make migrations
```
$ python manage.py makemigrations # In ./backend folder
```
5. Compile the js files (optional)
```
$ npm run build:all # In ./frontend folder
```
6. Run Django server and nodejs server side render
```
$ python manage.py runserver # In ./backend folder
# Open another terminal
$ npm run watch:server # In ./frontend folder
```
