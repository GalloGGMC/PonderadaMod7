FROM python:3.10
WORKDIR /back
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["fastapi", "run", "app.py"]