# Requests Redirect (Heroku Add-on)

A lightweight HTTP proxy Heroku Add-on built with Flask and SQLAlchemy.

This add-on allows Heroku users to seamlessly proxy traffic from their Heroku apps to a specific destination URL.

## How users install it

Users can provision your add-on to their app and specify the destination URL via the `--location` flag:

```bash
heroku addons:create requests-redirect --location=https://www.example.com
```

Once installed, Heroku will set a `REQUESTS_PROXY_URL` config variable in their application environment. 
Any requests sent to `REQUESTS_PROXY_URL/some-path` will be transparently forwarded to `https://www.example.com/some-path`.

To update the location later, users can run:
```bash
heroku addons:upgrade requests-redirect --location=https://www.new-example.com
```

## Running the Add-on Provider Server Locally

As the Add-on provider, you need to host this codebase so Heroku can communicate with it.

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with the credentials provided by the Heroku Partner Portal:
   ```dotenv
   HEROKU_ADDON_ID=your-addon-id
   HEROKU_ADDON_PASSWORD=your-addon-password
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
