
FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY . /app/ocr
WORKDIR /app/ocr

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN pip install --upgrade pip \
    && pip install  -r requirements.txt

EXPOSE 666
CMD python app.py


