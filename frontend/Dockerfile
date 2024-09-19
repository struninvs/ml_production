# Используем базовый образ
FROM ubuntu:latest

# Устанавлиаем Conda
RUN apt-get update && apt-get install -y wget bzip2
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py311_24.1.2-0-Linux-x86_64.sh -O miniconda.sh
RUN /bin/bash miniconda.sh -b -p /opt/conda
RUN rm miniconda.sh

ENV PATH="/opt/conda/bin:$PATH"

# Создаем файл .condarc и добавляем каналы
RUN echo "channels:" >> /root/.condarc
RUN echo "  - defaults" >> /root/.condarc
RUN echo "  - conda-forge" >> /root/.condarc

COPY environment.yml .

RUN conda update conda \
    && conda install -c anaconda pip \
    && pip install --upgrade pip \
    && python -m pip cache purge

RUN conda env update --name root --file environment.yml

COPY ./src/ frontend/src/

ARG FRONTEND_PORT

EXPOSE $FRONTEND_PORT

ENTRYPOINT ["python", "frontend/src/run.py"]