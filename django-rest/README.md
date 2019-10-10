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


## Clean up
After running for a while, the application may generate some files in the `tmp` directory and some entries in the database that would not be used anymore. Use `python manage.py mycleanup` to clean up those things. For production, you should set up a service running this command daily to do the clean up job.


## Deploy production server

Since it is a django application, you can refer to [django deployment documents]( https://docs.djangoproject.com/en/2.2/howto/deployment/) to deploy in your way. The most common way might be using Apache + mod_wsgi:
- Install Apache and the mod_wsgi module (make sure the mod_wsgi is built for python3: you can build the mod_wsgi from source code and configure it with python3 if python3 is not the default python, such as `./configure --with-python=/bin/python3.6`)
- Add a site configure file such as 
```
LoadModule wsgi_module modules/mod_wsgi.so
Listen 8000
<VirtualHost *:8000>
    Alias /static /var/www/hjiang5/static
    <Directory /var/www/hjiang5/static>
        Require all granted
        Options None
    </Directory>
    <Directory /var/www/hjiang5/hcc-jobs/django-rest/config>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    SSLEngine On
    SSLCertificateFile yourcertfile
    SSLCertificateKeyFile yourkeyfile

    SetEnv DJANGO_SECRET_KEY yoursecretstring

    WSGIDaemonProcess django-rest python-path=/var/www/hjiang5/hcc-jobs/django-rest:/var/www/hjiang5/hcc-jobs/django-rest/venv/lib/python3.6/site-packages
    WSGIProcessGroup django-rest
    WSGIScriptAlias / /var/www/hjiang5/hcc-jobs/django-rest/config/wsgi.py
</VirtualHost>
```
- Make sure the `TEMP_DIR` under your static directory with name `tmp`, and its permission for others should be `--x`, which means it is not readable but accessible by others. Also, make sure the static directory is not indexable. 
- Make sure your database file such as `db.sqlite3` is not readable by others.
- Make sure the apache config file is not readible by others.


## Deploy on multiple clusters

To deploy it on multipe clusters, make sure they are using the same LDAP to save user accounts. And, instead of sqlite, you need another kind of database such as mysql or postgres, and this database needs to be shared by the multiple django applications running on the clusters. To make sure the database only be accessible by your django applications, you probably need to set the database credentials in environment variables and then use them in your application. When deploying with Apache, you need to `SetEnv` in config file and pass them in the file `config/wsgi.py` just like the `DJANGO_SECRET_KEY` environment variable.
