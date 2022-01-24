FROM python:3.8
LABEL maintainer="codyzacharias@pm.me"

WORKDIR /root

RUN git clone --depth=1 https://github.com/twintproject/twint.git && \
	cd /root/twint && \
	pip install . -r requirements.txt

CMD /bin/bash