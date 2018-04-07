# GoodMatesServer

1. Download Python 2.7 https://www.python.org/downloads/release/python-2714/
2. Make sure that your system environment's PATH variable includes C:\Python27 and C:\Python27\Scripts
3. `python get-pip.py`
4. Reopen the terminal
5. `pip install -r requirements.txt`


# Run the Server:

`python manage.py runserver 0.0.0.0:80`

Access in web browser at: localhost

End server with Ctrl+C

# File Structure in Django

## `src/src`

### settings.py

File that just sets a bunch of options like where we're serving static files from or if we're in debug mode. Generally not going to use in project.

### urls.py

This defines urls using a regular expression and routes them to a 'View'.

If you use a capturing group in the regex, you need it start with `?P<varname>` so it can pass invoke view(request, varname=captured_value). ex: `(?P<year>[0-9]{4})` will call view(request, year='2018') if you input 2018.

In this project, we don't need to do anything fancy with urls.py, so each entry can be:

`url(r'^url/endpoint/$', view)`

Where view is a function from views.py

### wsgi.py

Never touched this file. You don't need to concern yourself with this.

## `src/GoodMatesServer`