# slim-buster is significantly smaller, but to compensate it excludes certain tools such as gcc (which may be needed to build certain dependencies)
# For now I will use the buster image until I discover valid ways of reducing both image size and build time

FROM python:3.9.7-buster

RUN apt-get -y update

RUN apt-get -y install git

WORKDIR /home

RUN git clone https://github.com/yamaan93/Engineering-Support-Bot.git

WORKDIR /home/Engineering-Support-Bot

RUN pip install -r requirements.txt

COPY botkey.txt .

COPY client_secret.json .

COPY currentWeek.xlsx .

COPY current_schedule.xlsx .

COPY beef.xlsx .

CMD ["python", "-u", "bot.py"]
