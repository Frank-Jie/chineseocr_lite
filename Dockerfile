
FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY . /app/coral_ocr
WORKDIR /app/coral_ocr

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN pip install --upgrade pip && pip install  -r requirements.txt


ENTRYPOINT ["gunicorn","-c", "gunicorn.py", "app:app"]




