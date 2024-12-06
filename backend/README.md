# FastAPI backend

## What to change
Changes are explained in the root README.md

## How to start
### Without docker
1. Set up the mysql connection string in `./database/loader.py` or set the needed env vars
2. In `bot/loader.py` change the token and add your telegram id to the `admins` list
3. Install the requirements
    ```bash
    python -m venv venv
    ./venv/Source/activate
    pip install -r requirements
    ```
4. Start the server
    ```bash
   python3 main.py
   ```
5. Start bot
    ```bash
    python3 bot_main.py
    ```

The server is now running on `http://0.0.0.0:3001` and the bot is running on the telegram bot token you provided

### With docker
Instructions are in the root README.md