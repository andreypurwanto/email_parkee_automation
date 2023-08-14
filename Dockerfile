FROM python:3.8.13-slim-buster as builder

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip python3-dev \
    python3-setuptools gfortran liblapack-dev liblapack3 nano \
    supervisor locales \
    && python3 -m venv /opt/venv

COPY requirements.txt .
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.8.13-slim-buster as run

ARG APP_USER="parkee_automation_hore"
ARG WORK_DIRECTORY="/app"
ARG TZ="Asia/Jakarta"

COPY . /app
WORKDIR $WORK_DIRECTORY

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends libgomp1 locales dumb-init \
    && useradd -rm -d $WORK_DIRECTORY -s /bin/bash -U $APP_USER \
    && chown -R $APP_USER:$APP_USER $WORK_DIRECTORY \
    && locale-gen en_US.UTF-8 \
    && export LC_ALL=en_US.UTF-8 \
    && export LANG=en_US.UTF-8 \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone \
    && apt-get clean 
    # && apt-get install -y wkhtmltopdf 

RUN apt -y install ./static/wkhtmltox_0.12.6-1.buster_amd64.deb

# USER $APP_USER

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="${WORK_DIRECTORY}:$PYTHONPATH"

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
# CMD ["python3"]