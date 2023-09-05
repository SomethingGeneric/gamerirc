FROM python:3.11.5-alpine3.17
RUN apk add git curl traceroute whois nmap wget figlet bc openssh bash
WORKDIR /bot
COPY . .
RUN pip3 install -r requirements.txt
RUN mkdir -p /root/.ssh
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN mv /bot/gb /root/.ssh/id_rsa
RUN mv /bot/gb.pub /root/.ssh/id_rsa.pub
RUN chmod -R 600 /root/.ssh
CMD ["python3", "main.py"]