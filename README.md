# hcc-jobs
A simple cluster web portal for HCC.

The `django-rest` folder contains the backend code, which is a [Django](https://www.djangoproject.com) application in python. It runs on the a cluster node and simply provides a Restful API for the frontend application. Fully decoupled from the frontend, it could be deployed on multiple clusters and provide the API independently.

The `client` folder contains the frontend code, which is a single-page [Vue](https://vuejs.org/) application. It consumes the Restful API(s) from the backend(s) and provides a uniform web interface for users.

There are mainly four functions provided:
- User authorization by LDAP
- View and operate slurm jobs, monitor running job performance (CPU and memory usage) 
- View and operate cluster file system
- Launch Jupyter notebook on cluster

Please refer to the README inside the two folders for details.
