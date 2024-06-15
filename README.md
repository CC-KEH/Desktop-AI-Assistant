# Requirements

## Python 3.11.2

## Setup

## After cloning run the following commands

    `pip install -r requirements.txt`
    `touch .env`
    System requirements: 
    `choco install visualcpp-build-tools`

## Google API Setup

### Create a google [developer account](https://console.developers.google.com/)

1. Go to Dashboard, create Project, fill details, enable the required APIs
2. Go to Credentials, create OAuth 2.0 Client ID, fill details, add http://localhost/4000 in RedirectURL
3. API and Services -> Library -> **Enable**: Google Calendar API, Google Drive API, Google mail API.
4. After creating OAuth 2.0 Client ID, download the credentials.json and replace it with the credentials.json in the connections folder
5. Once you run the main.py, it will ask you to login to your google account, login and it will redirect you to localhost, copy the url and paste it in the terminal

---

## Spotify Setup

### Create a spotify [developer account](https://developer.spotify.com/)

1. Go to Dashboard, create App, fill details, ignore Website box, write http://localhost/4000 in RedirectURL

2. After creating app Get client id, client secret and replace it with the clientID, clientSecret in main.py

3. Once you run the main.py, it will ask you to login to your spotify account, login and it will redirect you to localhost, copy the url and paste it in the terminal

4. Now the assistant is connected to your spotify account

---

## Gemini API Setup

### Visit [Gemini](https://ai.google.dev/)

1. Sign in with your google account
2. Select your project in Google cloud and make sure to enable the Generative Language API.
3. Copy the API key and replace it with the API key in the .env file

---

## Notion API Setup

### Create a notion [developer account](https://www.notion.so/my-integrations)

1. Go to Integrations, create a new integration, fill details, enable the required permissions
2. After creating the integration, copy the token and replace it with the token in the .env file
3. This program works with 4 databases: movies, animes, books, tasks. You will have to create these databases on your Notion, copy their database id, and put it in the .env file.
4. For reference, you can check this amazing blog on [How to use Python with Notion API](https://dev.to/mihaiandrei97/how-to-use-python-with-notion-api-1n61)  

---

### Architecture

```ascii

  +----------+           +--------+          +---------+           +--------+
  |          |           |        |          |         |           |        |
  |          |----------→|        |←--------→|         |----------→|        |
  |          |           |        |          |         |           |        |
  |   User   |           |  Main  |          | ChatBot |           | System |
  | (Speaks) |           |        |---------→|         |           |        |
  |          |←----------|        |←---------|         |←----------|        |
  |          |           |        |          |         |           |        |
  +----------+           +--------+          +---------+           +--------+
                                                                     |   ↑
                                                                     |   |
                                                                     |   |
                                                                     ↓   |
                                                                  +----------+
                                                                  |          |
                                                                  |  Gemini  |
                                                                  |          |
                                                                  +----------+


```
