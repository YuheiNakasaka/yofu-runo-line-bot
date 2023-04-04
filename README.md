# yofu-runo-line-bot

![IMG_4255_res (1)](https://user-images.githubusercontent.com/1421093/229732548-4e1934cc-7db8-4d4e-b875-0fa5ea3b7794.png)

# Requirements

```
% python3 --version
Python 3.9.13
```

```
% pip install black beautifulsoup4
% pip install -r requirements.txt
% brew install flyctl
```

```
% vim .env
OPENAI_API_KEY=
LINE_CHANNEL_SECRET=
LINE_CHANNEL_ACCESS_TOKEN=
```

# Usage

## Local

```
% uvicorn main:app --reload
% open localhost:8080
```

## Deploy

```
% flyctl auth login
% flyctl launch
% flyctl deploy
```
