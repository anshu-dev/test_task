## How To Start ?

### Install RabitMQ Server For Celery
```
sudo apt-get update -y
sudo apt-get install curl gnupg -y
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get install apt-transport-https
sudo apt-get update -y
sudo apt-get install rabbitmq-server -y --fix-missing
```

### Prepare tech_test

1. Create a virtual environment with pyenv or whatever you want
2. Activate the virtual environment
3. Execute the following command: pip install -r requirements.txt
4. Execute the migrations of django follow the command **python manage.py migrate**
5. Now, run the project: **python manage.py runserver**


### Configure a Celery Task


- Run below command at project root directory to start celery worker for receive task
```
celery -A tech_test worker --loglevel=INFO
```

#### Endpoints

- To Upload files - http://localhost/upload/
- To Fetch Building Info - http://localhost/buildings/
- To Fetch Meters Info - http://localhost/buildings/<int:pk>/meters/
- To Fetch Half Hourly Data Info - http://localhost/buildings/<int:pk>/meters/<int:meter_id>/half-hourly-data/
- To Show Graph - http://localhost/meter/<int:pk>/show-chart/