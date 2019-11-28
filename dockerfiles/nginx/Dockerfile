# Stage 1 - Use Django to collect
# all static files
FROM python:3.7 AS python

WORKDIR /usr/local-library

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add application
COPY ./catalog ./catalog
COPY ./locallibrary ./locallibrary
COPY ./manage.py ./manage.py

# Collect static files
RUN python3 manage.py collectstatic --no-input

# Stage 2 - nginx
FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/django.conf
COPY --from=python /usr/local-library/locallibrary/static /www/locallibrary/static
