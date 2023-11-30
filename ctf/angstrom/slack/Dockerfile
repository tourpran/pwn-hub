FROM ubuntu:22.04

RUN useradd -m ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf

COPY slack .
COPY flag.txt .
COPY ynetd .
COPY libc.so.6 .
COPY ld-linux-x86-64.so.2 .

RUN chown -R root:root /home/ctf
RUN chmod -R 555 /home/ctf

USER ctf
EXPOSE 1338
CMD ./ynetd -p 1338 ./slack