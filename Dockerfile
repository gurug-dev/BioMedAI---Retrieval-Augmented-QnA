FROM python:3.9.5

RUN pip install -U pip 


# This line is necessary in order to install spacy
RUN apt-get update && apt-get install -y python3-dev build-essential
RUN apt-get -y install git
WORKDIR /app

COPY [ "requirements.txt", "./" ]

RUN pip install -r requirements.txt
RUn pip install detectron2@git+https://github.com/facebookresearch/detectron2.git@d1e04565d3bec8719335b88be9e9b961bf3ec464

COPY . .

EXPOSE 8000

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]