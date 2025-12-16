FROM --platform=$BUILDPLATFORM python:3.13.0

WORKDIR /app

# set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install the requirements
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .
# RUN flask db upgrade
EXPOSE 5000/tcp

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
#CMD ["python","main.py"]