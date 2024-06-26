FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code


RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin libgdal-dev libgeos-dev \
    && rm -rf /var/lib/apt/lists/* 
    

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

RUN addgroup --system app && adduser --system --ingroup app aidlatifaj
RUN id aidlatifaj && groups aidlatifaj

RUN mkdir -p /staticfiles /media /nonexistent
RUN mkdir -p /etc/sudoers.d && echo "aidlatifaj ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/aidlatifaj

RUN chown -R aidlatifaj:app /staticfiles /media /nonexistent /code


USER aidlatifaj

EXPOSE 8000

CMD ["uvicorn", "busstation.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
