FROM python:3.10
WORKDIR /front
COPY . .
RUN pip3 install -r requirements.txt
CMD ["streamlit", "run", "front.py"]