FROM python:3.9
COPY ./requirements.txt /var/www/requirements.txt
RUN pip3 install -r /var/www/requirements.txt
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL en_PH.UTF-8
ENV LANG en_PH.UTF-8
ENV LANGUAGE en_PH.UTF-8
