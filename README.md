# Locust Load Testing Project

This project utilizes Locust, an open-source load testing tool, to simulate users interacting with a specific API endpoint.

## Getting Started

### Prerequisites

- Docker installed on your machine.

### Running the Project

Run:
```
docker-compose up --build
```

Stop:
```
docker-compose down
```

Web UI will be available on http://localhost:8089

After run, report will be available in [src/report.html](./src/report.html)

## Customization

You can customize the load test by modifying the environment variable in [.env](.env) file and [docker-compose.yml](./docker-compose.yml), like `WAIT_TIME` when running the Docker container. This variable determines the wait time between each task executed by the simulated users.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project or add new features.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
