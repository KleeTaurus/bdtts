# bdtts
Baidu TTS for IP Subscription Project

# Installation

1. setup virtualenv and activate it
```
python -m venv venv
source venv/bin/activate
```

2. install python-dotenv
```
pip install python-dotenv
```

3. create .env file and set API_KEY and SECRET_KEY
```
touch .env
vi .env
```

API_KEY=<YOUR_API_KEY>
SECRET_KEY=<YOUR_SECRET_KEY>

4. download ffmpeg binary file into current directory
```
wget https://evermeet.cx/ffmpeg/ffmpeg-113507-gf6b7b473d4.zip
unzip ffmpeg-113507-gf6b7b473d4.zip
```

# Usage

copy your text into input.txt

convert text into audio(wav)

```
./run.sh
```
