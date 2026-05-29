# Antarctic Weather Intelligence

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Tests](https://img.shields.io/badge/Tests-Passing-success)


Backend API developed with FastAPI for retrieving, aggregating and caching Antarctic weather data.



## Overview



This project was developed as part of the GS Inima Python Web API Challenge.



The service provides historical weather data for Antarctic meteorological stations, supporting:



* Temperature

* Pressure

* Wind Speed



The API supports multiple aggregation levels, SQLite caching, timezone conversion, Docker deployment and automated tests.



---



## Features



### Weather Data Retrieval



Retrieve historical weather data for:



* Gabriel de Castilla Station

* Juan Carlos I Station



### Aggregations



Supported aggregation levels:



* none

* hourly

* daily

* monthly



### Timezone Handling



All output datetimes are returned in:



Europe/Madrid (CET/CEST)



including the UTC offset.



### SQLite Cache



To avoid excessive requests to the external weather provider:



* Data is stored locally in SQLite

* Cache hit/miss strategy implemented

* Previously requested data is served directly from cache



### Field Selection



Users may select:



* temperature

* pressure

* wind\_speed



Example:



```http

?fields=temperature,pressure

```



\### Automated Tests



Implemented with pytest.



Current coverage includes:



* Station validation

* Timezone conversion

* Aggregation logic

* Weather service utilities



---



## Architecture



```text

app/

├── api/

│   └── routes.py

│

├── core/

│   ├── constants.py

│   └── timezone.py

│

├── db/

│   └── database.py

│

├── models/

│   └── weather\_observation.py

│

├── schemas/

│   └── weather.py

│

├── services/

│   ├── weather\_service.py

│   └── open\_meteo\_client.py

│

└── main.py

```



---



## Installation



### Create virtual environment



```bash

python -m venv .venv

```



### Activate



Windows:



```bash

.venv\\Scripts\\activate

```



### Install dependencies



```bash

pip install -r requirements.txt

```



---



## Running Locally



```bash

uvicorn app.main:app --reload

```



Swagger:



```text

http://127.0.0.1:8000/docs

```



---



## Docker



Build and run:



```bash

docker compose up --build

```



Swagger:



```text

http://127.0.0.1:8001/docs

```



---



## Example Requests



### Daily Aggregation



```http

GET /api/antarctica/data/start/2024-01-01T00:00:00/end/2024-01-10T00:00:00/station/gabriel?aggregation=daily

```



### Monthly Aggregation



```http

GET /api/antarctica/data/start/2024-01-01T00:00:00/end/2024-03-31T00:00:00/station/gabriel?aggregation=monthly

```



### Temperature Only



```http

GET /api/antarctica/data/start/2024-01-01T00:00:00/end/2024-01-10T00:00:00/station/gabriel?aggregation=daily\&fields=temperature

```



---



## Cache Strategy



Request flow:



```text

Client

&#x20; ↓

SQLite Cache

&#x20; ↓

Cache Hit ? ── Yes → Return Cached Data

&#x20; ↓ No

Open-Meteo API

&#x20; ↓

Store in SQLite

&#x20; ↓

Return Response

```



---



## Daylight Saving Time (DST)



The service converts all output timestamps to:



Europe/Madrid



Examples:



Winter:



```text

UTC+1

```



Summer:



```text

UTC+2

```



Tests validate DST behavior.



---



## Testing



Run all tests:



```bash

pytest

```



Current status:



```text

7 tests passed

```



---



## Future Improvements



* Frontend dashboard with React + TypeScript

* Charts for weather visualization

* PostgreSQL support

* Redis cache layer

* CI/CD pipeline with GitHub Actions

* Extended station catalogue



---



## Technologies



* Python 3.13

* FastAPI

* SQLAlchemy

* SQLite

* Pydantic

* Pytest

* Docker

* Open-Meteo API

* Loguru

## Project Status



This project was originally developed as part of the GS Inima Python Web API Challenge.



Current implementation includes:



* Historical weather retrieval

* SQLite cache layer

* Daily and monthly aggregations

* Timezone conversion

* Docker deployment

* Automated tests

* OpenAPI / Swagger documentation



Future iterations may include a React frontend, Redis caching, PostgreSQL support and CI/CD automation.



