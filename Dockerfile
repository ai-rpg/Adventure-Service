FROM python:3.11-slim-buster
COPY /src .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
# RUN pipenv install --dev

EXPOSE 9899
WORKDIR app
CMD ["python", "main.py"]