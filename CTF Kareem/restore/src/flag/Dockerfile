FROM debian:bookworm-slim
RUN echo "SENSITIVE" > secret.txt
RUN echo "NOT REALLY" > flag.txt 
COPY flag.txt /flag.txt
RUN rm -rf secret.txt flag.txt
USER ctf
CMD ["sleep", "infinity"]