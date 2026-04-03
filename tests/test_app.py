from app import create_app


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "service": "platform-log-service",
        "status": "running-ok"
    }


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy"
    }


def test_logs_returns_only_error_lines(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "INFO app started\n"
        "ERROR database connection failed\n"
        "WARNING retrying\n"
        "ERROR timeout occurred\n"
    )

    app = create_app()
    app.config["TESTING"] = True
    app.config["LOG_FILE"] = str(log_file)

    client = app.test_client()
    response = client.get("/logs")

    assert response.status_code == 200
    assert response.get_json() == {
        "error_count": 2,
        "errors": [
            "ERROR database connection failed",
            "ERROR timeout occurred"
        ]
    }


def test_logs_file_not_found(tmp_path):
    missing_file = tmp_path / "missing.log"

    app = create_app()
    app.config["TESTING"] = True
    app.config["LOG_FILE"] = str(missing_file)

    client = app.test_client()
    response = client.get("/logs")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": f"Log file '{missing_file}' not found"
    }
