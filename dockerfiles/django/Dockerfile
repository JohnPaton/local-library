FROM python:3.7

WORKDIR /usr/local-library

# Show logs properly
ENV PYTHONUNBUFFERED=1

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Volume for application data (when using sqlite)
VOLUME /usr/local-library/data

# Add application
COPY catalog ./catalog/
COPY templates ./templates/
COPY locallibrary ./locallibrary/
COPY manage.py ./manage.py

# Collect static files (for gunicorn)
RUN python3 manage.py collectstatic --no-input --link

# Serve
EXPOSE 8000
CMD [ \
    "gunicorn", \
        "--bind", "0.0.0.0:8000", \
        "--worker-class", "eventlet", \
        "--keep-alive", "75", \
        "locallibrary.wsgi:application" \
]
