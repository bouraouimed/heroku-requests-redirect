# Requests Redirect Proxy (Heroku Add-on)

A lightweight, flexible HTTP proxy service built with Flask and Python. This project is currently being developed into a fully-fledged **Heroku Add-on** that allows applications to proxy HTTP requests through a dedicated service, providing centralized request forwarding, CORS handling, and strict host-based access controls.

## Features

- **Dynamic Request Proxying**: Transparently forwards all HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.) and payload data to a destination URL.
- **Configurable Access Controls**: Restrict incoming requests to specific clients using the `ALLOWED_HOST` configuration (verifying the origin, remote address, or host header).
- **Environment-Driven Configuration**: Easily configurable via `.env` files or Heroku Config Vars.
- **Heroku Add-on Ready (WIP)**: Being extended to support the Heroku Partner API for automated provisioning, deprovisioning, and seamless integration into any Heroku workflow.

## Configuration

This project relies on environment variables for configuration. You can create a `.env` file in the root directory:

```dotenv
# The target base URL where requests should be redirected
ROOT_DEST_URL=https://my-destination-server

# (Optional) The specific Host/Origin/IP allowed to make requests to this proxy
ALLOWED_HOST=127.0.0.1
```

## Running Locally

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
   *Alternatively, if using the Heroku CLI, you can run:*
   ```bash
   heroku local
   ```

## Next Steps

- Implement the Heroku Add-on Partner API endpoints (`POST /heroku/resources`, `DELETE /heroku/resources/:id`).
- Add Basic Authentication for the Add-on lifecycle events.
- Implement a database layer to track provisioned Heroku resources.
