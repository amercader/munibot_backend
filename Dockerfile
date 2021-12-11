FROM python:3.9

WORKDIR /opt/munibot
ENV MUNIBOT_CONFIG_FILE=/opt/munibot/munibot.ini

COPY ./requirements.txt ./munibot.ini /opt/munibot/

RUN pip install --no-cache-dir --upgrade -r /opt/munibot/requirements.txt

COPY ./app /opt/munibot/app

EXPOSE 9000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
