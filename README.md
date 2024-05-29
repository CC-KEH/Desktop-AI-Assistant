# Requirements

## Python 3.11.2

## Setup

## After cloning run the following commands

    `pip install -r requirements.txt`
    System requirements: 
    `choco install visualcpp-build-tools`

## Spotify Setup

### Create a spotify [developer account](https://developer.spotify.com/)

### Go to Dashboard, create App, fill details, ignore Website box, write http://localhost/4000 in RedirectURL

### After creating app Get client id, client secret and replace it with the clientID, clientSecret in main.py

### You are good to go

## OPENAI API Setup

### Visit [OpenAI](https://openai.com/)

### Credits

[How to use Python with Notion API](https://dev.to/mihaiandrei97/how-to-use-python-with-notion-api-1n61)

### Architecture

  +--------+           +--------+          +---------+           +--------+
  |        |---------->|        |--------->|         |           |        |
  |        |<----------|        |<---------|         |<--------->|        |
  |        |           |        |          |         |           |        |
  |  User  |           |  Main  |          | ChatBot |           | System |
  |        |           |        |          |         |           |        |
  |        |<----------|        |<---------|         |<--------->|        |
  |        |---------->|        |--------->|         |           |        |
  +--------+           +--------+          +---------+           +--------+
