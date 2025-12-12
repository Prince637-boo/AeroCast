
├── alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── docker
│   ├── entrypoint.sh
│   └── supervisord.conf
├── docker-compose.yml
├── libs
│   └── common
│       ├── base.py
│       ├── config.py
│       ├── database.py
│       ├── exceptions.py
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── base.cpython-314.pyc
│       │   ├── config.cpython-314.pyc
│       │   ├── database.cpython-314.pyc
│       │   ├── __init__.cpython-314.pyc
│       │   └── security.cpython-314.pyc
│       ├── security.py
│       └── utils.py
├── logstash
│   └── pipeline
│       └── logstash.conf
├── otel_collector.yml
├── prometheus.yml
├── __pycache__
│   └── conftest.cpython-314-pytest-9.0.2.pyc
├── pyproject.toml
├── README.md
├── services
│   ├── auth
│   │   ├── core
│   │   │   ├── hashing.py
│   │   │   ├── jwt.py
│   │   │   ├── __pycache__
│   │   │   │   ├── hashing.cpython-314.pyc
│   │   │   │   ├── jwt.cpython-314.pyc
│   │   │   │   └── roles.cpython-314.pyc
│   │   │   └── roles.py
│   │   ├── dependencies
│   │   │   ├── permissions.py
│   │   │   ├── __pycache__
│   │   │   │   ├── permissions.cpython-314.pyc
│   │   │   │   └── user.cpython-314.pyc
│   │   │   └── user.py
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── middleware
│   │   │   ├── logging.py
│   │   │   └── __pycache__
│   │   │       └── logging.cpython-314.pyc
│   │   ├── models
│   │   │   ├── company.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── company.cpython-314.pyc
│   │   │   │   ├── __init__.cpython-314.pyc
│   │   │   │   ├── refresh_token.cpython-314.pyc
│   │   │   │   └── user.cpython-314.pyc
│   │   │   ├── refresh_token.py
│   │   │   └── user.py
│   │   ├── otel_setup.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── main.cpython-314.pyc
│   │   │   └── service_user.cpython-314.pyc
│   │   ├── README.md
│   │   ├── routers
│   │   │   ├── auth.py
│   │   │   └── __pycache__
│   │   │       └── auth.cpython-314.pyc
│   │   ├── schemas
│   │   │   ├── company.py
│   │   │   ├── __pycache__
│   │   │   │   ├── company.cpython-314.pyc
│   │   │   │   └── user.cpython-314.pyc
│   │   │   └── user.py
│   │   └── service_user.py
│   ├── baggage
│   │   ├── baggage_service.py
│   │   ├── core
│   │   │   ├── enums.py
│   │   │   ├── event.py
│   │   │   ├── __pycache__
│   │   │   │   ├── enums.cpython-314.pyc
│   │   │   │   └── utils.cpython-314.pyc
│   │   │   └── utils.py
│   │   ├── dependencies
│   │   ├── Dockerfile
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── metrics.py
│   │   ├── models
│   │   │   ├── baggage_event.py
│   │   │   ├── bag.py
│   │   │   ├── __pycache__
│   │   │   │   ├── bag.cpython-314.pyc
│   │   │   │   ├── baggage_event.cpython-314.pyc
│   │   │   │   └── scan_log.cpython-314.pyc
│   │   │   └── scan_log.py
│   │   ├── otel_setup.py
│   │   ├── __pycache__
│   │   │   ├── baggage_service.cpython-314.pyc
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── main.cpython-314.pyc
│   │   │   └── otel_setup.cpython-314.pyc
│   │   ├── README.md
│   │   ├── redis
│   │   │   ├── __init__.py
│   │   │   └── redis_c.py
│   │   ├── routers
│   │   │   ├── admin.py
│   │   │   ├── baggages.py
│   │   │   ├── gps.py
│   │   │   ├── __pycache__
│   │   │   │   ├── admin.cpython-314.pyc
│   │   │   │   ├── baggages.cpython-314.pyc
│   │   │   │   └── ws.cpython-314.pyc
│   │   │   ├── trackers.py
│   │   │   └── ws.py
│   │   ├── schemas
│   │   │   ├── baggage_event.py
│   │   │   ├── bag.py
│   │   │   ├── __pycache__
│   │   │   │   ├── bag.cpython-314.pyc
│   │   │   │   ├── baggage_event.cpython-314.pyc
│   │   │   │   └── scan_log.cpython-314.pyc
│   │   │   └── scan_log.py
│   │   └── worker
│   │       └── consumer.py
│   ├── __init__.py
│   ├── orientation
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── decision_engine.py
│   │   │   ├── __init__.py
│   │   │   ├── path_optimizer.py
│   │   │   └── __pycache__
│   │   │       ├── config.cpython-314.pyc
│   │   │       ├── decision_engine.cpython-314.pyc
│   │   │       └── __init__.cpython-314.pyc
│   │   ├── dependencies
│   │   │   ├── __pycache__
│   │   │   │   ├── services.cpython-314.pyc
│   │   │   │   └── validation.cpython-314.pyc
│   │   │   ├── services.py
│   │   │   └── validation.py
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── middleware
│   │   │   ├── logging.py
│   │   │   └── __pycache__
│   │   │       └── logging.cpython-314.pyc
│   │   ├── models
│   │   │   └── orientation.py
│   │   ├── __pycache__
│   │   │   ├── main.cpython-314.pyc
│   │   │   └── utils.cpython-314.pyc
│   │   ├── README.md
│   │   ├── routers
│   │   │   ├── orientation.py
│   │   │   └── __pycache__
│   │   │       └── orientation.cpython-314.pyc
│   │   ├── schemas
│   │   │   ├── orientation.py
│   │   │   └── __pycache__
│   │   │       └── orientation.cpython-314.pyc
│   │   ├── services
│   │   │   ├── baggage_client.py
│   │   │   ├── meteo_client.py
│   │   │   ├── __pycache__
│   │   │   │   ├── baggage_client.cpython-314.pyc
│   │   │   │   ├── meteo_client.cpython-314.pyc
│   │   │   │   └── vol_client.cpython-314.pyc
│   │   │   └── vol_client.py
│   │   └── utils.py
│   ├── __pycache__
│   │   └── __init__.cpython-314.pyc
│   └── weather
│       ├── config.py
│       ├── crud
│       ├── dependencies
│       │   ├── __pycache__
│       │   │   └── weather_deps.cpython-314.pyc
│       │   └── weather_deps.py
│       ├── Dockerfile
│       ├── __init__.py
│       ├── main.py
│       ├── models
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   │   ├── __init__.cpython-314.pyc
│       │   │   └── weather.cpython-314.pyc
│       │   └── weather.py
│       ├── __pycache__
│       │   ├── config.cpython-314.pyc
│       │   ├── __init__.cpython-311.pyc
│       │   ├── __init__.cpython-314.pyc
│       │   ├── main.cpython-311.pyc
│       │   ├── main.cpython-314.pyc
│       │   ├── service_weather.cpython-314.pyc
│       │   └── test_orientation.cpython-314-pytest-9.0.2.pyc
│       ├── README.md
│       ├── redis_client.py
│       ├── routers
│       │   ├── __pycache__
│       │   │   └── weather.cpython-314.pyc
│       │   └── weather.py
│       ├── schemas
│       │   ├── open_meteo.py
│       │   ├── __pycache__
│       │   │   ├── open_meteo.cpython-314.pyc
│       │   │   └── weather.cpython-314.pyc
│       │   └── weather.py
│       ├── services
│       │   ├── __init__.py
│       │   ├── open_meteo.py
│       │   └── __pycache__
│       │       ├── __init__.cpython-314.pyc
│       │       └── open_meteo.cpython-314.pyc
│       ├── service_weather.py
│       └── workers
│           └── tasks.py
├── tests
│   ├── auth
│   │   ├── __pycache__
│   │   │   └── test_auth_route.cpython-314-pytest-9.0.2.pyc
│   │   └── test_auth_route.py
│   ├── baggages
│   │   ├── __pycache__
│   │   │   ├── test_baggages_routes.cpython-314-pytest-9.0.2.pyc
│   │   │   ├── test_orientation.cpython-314-pytest-9.0.2.pyc
│   │   │   └── test_ws.cpython-314-pytest-9.0.2.pyc
│   │   ├── test_baggages_routes.py
│   │   └── test_ws.py
│   ├── conftest.py
│   ├── __init__.py
│   ├── orientation
│   │   ├── __pycache__
│   │   │   └── test_orientation_routes.cpython-314-pytest-9.0.2.pyc
│   │   └── test_orientation_routes.py
│   ├── __pycache__
│   │   ├── conftest.cpython-314-pytest-9.0.2.pyc
│   │   ├── __init__.cpython-314.pyc
│   │   └── test_orientation.cpython-314-pytest-9.0.2.pyc
│   ├── test_orientation.py
│   ├── utils
│   │   ├── db.py
│   │   ├── http.py
│   │   └── __pycache__
│   │       ├── db.cpython-314.pyc
│   │       └── http.cpython-314.pyc
│   └── weather
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-314.pyc
│       │   └── test_weather.cpython-314-pytest-9.0.2.pyc
│       └── test_weather.py
├── traefik
│   └── dynamic.yml
└── uv.lock
