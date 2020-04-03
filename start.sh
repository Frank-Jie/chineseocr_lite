
gunicorn -c gunicorn.py app:app &

celery worker -A celery_tasks.main -l info -f /opt/hrms/logs/celery.log