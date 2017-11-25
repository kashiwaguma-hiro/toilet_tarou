FROM python:3.6

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]
CMD [ "tail", "-f", "/dev/null" ]
