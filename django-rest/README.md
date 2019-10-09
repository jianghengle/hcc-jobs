# Django Backend

The backend is a [Django](https://www.djangoproject.com/) project. It provides purely a Restful API server to be consumed by any other applications.

The backend should run on a Linux cluster node with the file system, LDAP and Slurm loaded, and with Jupyter notebook installed.

## Run development server

``` bash
# Use python3 create virtual environment
python3 -m venv venv

# Activate the virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Set environment variable
export DJANGO_SECRET_KEY=yoursecretstring

# Run django development server
python manage.py migrate

# Run django development server
python manage.py runserver
```

If you are running it on the cluster node and try to debug it, you probably want to change the `DEBUG` variable in `config/settings.py` to be `TRUE` and run the development server with `python manage.py runserver 0:8000` and make sure the `8000` port is opened.

To hook the client application to the development server, modify `servers` in the file `client/src/store/modules/info.js` to point to the development server ip and port.


## Settings

The Django application settings are in the file `config/settings.py`:
- `ALLOWED_HOSTS`: Update it reflect your server
- `TEMP_DIR`: Set it to a directory on your server to save some application temporal files. Make its name be `tmp` and under your server's static directory, since some files need be served from here. Also update the `STATICFILES_DIRS` to reflect your setting.
- `JUPYTER_PORTS`: This is to define the port range to be used by users' Jupyter notebooks. It also determines how many Jupyter notebooks you allow to be launched. Make sure those ports are opened.

