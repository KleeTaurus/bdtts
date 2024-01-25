# bdtts
Baidu TTS for IP Subscription Project

# Installation

setup virtualenv and activate it
```
python -m venv venv
source venv/bin/activate
```

install python-dotenv
```
pip install python-dotenv
```

create .env file and set API_KEY and SECRET_KEY
```
touch .env
vi .env
```

API_KEY=<YOUR_API_KEY>
SECRET_KEY=<YOUR_SECRET_KEY>

# Usage

copy your text into input.txt

convert text into audio(wav)

```
python tts.py
```
