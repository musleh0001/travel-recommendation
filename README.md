<div align="center">
    <h1>🌤️ Travel Recommendation API</h1>
</div>

<div align="center">
    <img src="https://img.shields.io/badge/Python-3.10-green" />
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json"/>
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" />
    <img src="https://code.lefttravel.com/vrs/backend/etl-vrs-analytics/badges/development/pipeline.svg" />
    <img src="https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white" />
</div>

---

### Prerequisites
- Python >= 3.10
- uv [recommended] or pip

### Project Setup:
```shell
1. git clone https://github.com/musleh0001/travel-recommendation
2. cd travel-recommendation
3. cp .env.example .env # update .env file
4. Create and Activate virtual env
5. Install requirements
6. bash entrypoint.sh
```

### For API documentations visit: `http://localhost:8000/swagger/`

<p>
    <b style="color: red">Warning:</b> Please do not edit <b>requirements.txt</b> manually.
</p>


##### Create virtual environment
```shell
uv venv [recommended]

or 

python3 -m venv .venv
```

##### Activate virtual environment
```shell
source .venv/bin/activate
```


##### Run server
```shell
python manage.py runserver
```

##### To add new libraries first update `pyproject.toml`.
```shell
uv pip compile pyproject.toml -o requirements.txt
```

##### Install libraries 
```shell
uv pip sync requirements.txt

or 

pip install -r requirements.txt
```

##### Apply Code Formate
```shell
ruff format .
```

##### Check linting
```shell
ruff check .
```

##### Run Test (Unit)
```shell
pytest
```


## API Endpoints
1. `POST` `/api/v1/auth/SignUp/` SignUp User
```json
request_body = {
    "username": "test",
    "email": "test@gmail.com",
    "password": "mypasswd"
}

response = {
    "username": "test",
    "email": "test@gmail.com"
}
```

2. `POST` `/api/v1/auth/token/` Generate JWT Token
```json
request_body = {
    "username": "test",
    "password": "mypasswd"
}

response = {
    "refresh": "test-refresh-token",
    "access": "test-access-token"
}
```

3. `POST` `/api/v1/auth/token/refresh/` Refresh Token
```json
request_body = {
    "refresh": "test-refresh-token"
}

response = {
    "refresh": "test-refresh-token",
    "access": "test-access-token"
}
```

4. `GET` `/api/v1/top_districts/` Get Top 10 districts
```json
headers = {
  "Authorization": "Bearer <test-access-token>"
}

response = [
    {
        "district": "Dhaka",
        "avg_temperature": 25.5038572038923,
        "avg_air_quality": 59.78099179859004
    }
]
```

5. `POST` `/api/v1/recommend_travel/` Get recommendation
```json
headers = {
  "Authorization": "Bearer <test-access-token>"
}

request_body = {
    "latitude": 23.7115253,
    "longitude": 90.4111451,
    "destination_district": "Dhaka",
    "travel_date": "2025-04-15"
}

response = {
    "recommendation": "Recommended",
    "reason": "Your destination is 0.9°C cooler and has better air quality. Enjoy your trip!"
}
```