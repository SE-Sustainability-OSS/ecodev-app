###########
# BUILDER #
###########
FROM python:3.11-slim as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install packages
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN python3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########
FROM python:3.11-slim

# Install build packages
COPY --from=builder /app/wheels /wheels
RUN python3 -m pip install --no-cache /wheels/*

## Ship code
COPY app/ /app/app
WORKDIR /app

#Opened ports
EXPOSE 80

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.dash_app:server", "--host", "0.0.0.0", "--port", "80", "--timeout-keep-alive", "300", "--ws-ping-timeout", "300" ]
