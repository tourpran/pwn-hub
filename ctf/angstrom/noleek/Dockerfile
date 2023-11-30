FROM debian@sha256:98d3b4b0cee264301eb1354e0b549323af2d0633e1c43375d0b25c01826b6790

RUN useradd -m ctf
RUN echo "ctf:ctf" | chpasswd
WORKDIR /home/ctf

COPY noleek .
COPY flag.txt .
COPY ynetd .

RUN chown -R root:root /home/ctf
RUN chmod -R 555 /home/ctf

USER ctf
EXPOSE 1337
CMD ./ynetd -p 1338 ./noleek