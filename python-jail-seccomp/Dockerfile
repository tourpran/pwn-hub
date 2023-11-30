FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y install socat python3
RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/ctf
RUN echo "ACSC{*** REDACTED ***}" > flag.txt
ADD app.py .
ADD seccomp.cpython-310-x86_64-linux-gnu.so .
RUN chmod 440 flag.txt
RUN chmod 550 app.py
RUN chmod 550 seccomp.cpython-310-x86_64-linux-gnu.so
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:ctf /home/ctf

USER ctf
CMD socat TCP-L:9999,reuseaddr,fork EXEC:"./app.py"
