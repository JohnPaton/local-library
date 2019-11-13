FROM python:3.7

WORKDIR /usr/local-library

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Volume for application data (when using sqlite)
VOLUME /usr/local-library/data

# Add application
COPY ./catalog ./catalog
COPY ./locallibrary ./locallibrary
COPY ./manage.py ./manage.py

# Serve
# TODO: Move to gunicorn
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
