# ML-модель в Production: от Jupyter до масштабируемого сервиса

## Описание
В данном репозитории представлен код проекта для вебинара в рамках воркшопа [ecom.tech](https://ecom.tech/) x [Deep Learning School](https://dls.samcs.ru/), который направлен на демонстрацию возможностей инструментов **Streamlit**, **FastAPI** и **Docker** для создания и продуктивизации решений машинного обучения (ML). Участники узнают, как легко и быстро разворачивать ML-приложения с помощью этих технологий, а также интегрировать их в рабочие процессы и контейнеризировать для дальнейшего использования:
* [Презентация для воркшопа в PDF](https://disk.yandex.ru/i/ikcYG-rQwR7iEw)
* [Ссылка на запись стрима VK](https://vk.com/dlschool_mipt?z=video-155161349_456239162%2Fvideos-155161349%2Fpl_-155161349_-2)
* Пример приложения в целях демонстрации развернут в [Streamlit Cloud](https://share.streamlit.io/) и доступен по адресу: https://dls-ml.streamlit.app

## Программа вебинара
1. **Streamlit** - создание простых и интерактивных интерфейсов для ML-моделей.
2. **FastAPI** - построение высокопроизводительных REST API для обслуживания моделей машинного обучения.
3. **Docker** - контейнеризация и развертывание ML-решений.

## Цели вебинара
- Познакомиться с основами Streamlit для быстрого прототипирования веб-приложений.
- Научиться строить API с FastAPI для интеграции моделей машинного обучения в различные приложения.
- Изучить основы работы с Docker для создания, тестирования и развертывания контейнеризованных ML-приложений.

## Требования
- Базовые знания Python и машинного обучения.
- Установленный Docker для работы с контейнерами.
- Опыт работы с библиотеками для машинного обучения (например, scikit-learn, TensorFlow, PyTorch).

## Структура проекта
- `.streamlit/` - конфигурационные файлы для Streamlit.
- `backend/` - директория с backend-частью на базе FastAPI:
  - `data/` - папка для данных backend.
  - `src/` - исходные файлы приложения:
    - `Dockerfile` - Docker-файл для backend.
    - `environment.yml` - описание окружения для backend.
- `frontend/` - директория с frontend-частью на базе Streamlit:
  - `data/` - папка для данных frontend.
  - `src/` - исходные файлы приложения:
    - `Dockerfile` - Docker-файл для frontend.
    - `environment.yml` - описание окружения для frontend.
- `scripts/` - директория со скриптами для сборки и запуска контейнеров:
  - `docker_backend_build.sh` - сборка Docker-образа для backend.
  - `docker_backend_run.sh` - запуск Docker-контейнера для backend.
  - `docker_clean.sh` - скрипт для очистки контейнеров и образов.
  - `docker_frontend_build.sh` - сборка Docker-образа для frontend.
  - `docker_frontend_run.sh` - запуск Docker-контейнера для frontend.
  - `docker_full.sh` - скрипт для сборки и запуска обоих сервисов (frontend и backend).
- `.env_sample.sh` - пример файла окружения.
- `.gitignore` - файл для исключения файлов и папок из Git.
- `environment.yml` - общее описание окружения проекта.
- `README.md` - файл с описанием проекта.
- `streamlit_app.py` - главный файл приложения Streamlit.


## Установка и запуск
1. **Клонируйте репозиторий**:
    ```bash
    git clone https://github.com/struninvs/ml_production.git
    cd ml-webinar
    ```
2. **Настройка переменных окружения**: Перед запуском приложений, скопируйте файл ```.env_sample.sh``` в ```.env.sh``` и отредактируйте его значения, если это необходимо:
    ```bash
    cp .env_sample.sh .env.sh
    ```
    * ```CONTAINER_NAME``` - имя контейнера.
    * ```CONTAINER_TAG``` - версия контейнера (по умолчанию latest).
    * ```BACKEND_HOST``` - хост для backend.
    * ```BACKEND_PORT``` - порт для backend (по умолчанию 8082).
    * ```FRONTEND_PORT``` - порт для frontend (по умолчанию 8083).
    * ```NETWORK_NAME``` - имя Docker-сети.
3. **Сборка и запуск контейнеров**:
  * Для запуска backend:
    ```bash
    ./scripts/docker_backend_build.sh
    ./scripts/docker_backend_run.sh
    ```
  * Для запуска frontend:
    ```bash
    ./scripts/docker_frontend_build.sh
    ./scripts/docker_frontend_run.sh
    ```
  * Для полной сборки и запуска:
    ```bash
    ./scripts/docker_full.sh
    ```
4. **Доступ к приложениям**:
  * Веб-интерфейс Streamlit будет доступен по адресу: http://localhost:8083
  * FastAPI будет доступен по адресу: http://localhost:8082

## Зачем использовать `docker_clean.sh`?

В процессе разработки с Docker могут накапливаться ненужные контейнеры и образы, что может привести к снижению производительности и заполнению диска. Скрипт `docker_clean.sh` помогает избежать этого, удаляя остановленные контейнеры, неиспользуемые образы, сети и тома. Регулярное использование этого скрипта поддерживает чистоту системы и улучшает её производительность.

Чтобы выполнить очистку, просто запустите скрипт:

```bash
./scripts/docker_clean.sh
```

# Дополнительные ресурсы
* [Streamlit документация](https://docs.streamlit.io/)
* [FastAPI документация](https://fastapi.tiangolo.com/ru/tutorial/#_1)
* [Docker документация](https://docs.docker.com/reference/cli/docker/)

# Контакты для связи

* [Струнин Владислав](https://t.me/struninvs) 