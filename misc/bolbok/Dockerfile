FROM ubuntu:rolling 

#RUN apt-get update \
#    && apt install openssh-server -y

RUN useradd bolbok -s /bin/rbash  \
    && echo "bolbok:x0101x" | chpasswd

RUN mkdir -p /usr/bolbok/bin

WORKDIR /home/bolbok

RUN echo "export PATH=/usr/bolbok/bin" >> /home/bolbok/.bashrc

RUN mkdir -p /var/users/bolbok/secrets/youwillneverfindthis/
COPY  flag.txt /var/users/bolbok/secrets/youwillneverfindthis/

#RUN echo "PermitRootLogin no" >> /etc/ssh/sshd_config &&\
#   echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

#RUN service ssh restart

RUN chown root:root /home/bolbok/.bashrc \
    && chmod 755 .bashrc

RUN ln -s /usr/bin/ls /usr/bolbok/bin/ \
    && ln -s /usr/bin/ps /usr/bolbok/bin/ \
    && ln -s /usr/bin/top /usr/bolbok/bin/ \
    && ln -s /usr/bin/uptime /usr/bolbok/bin/ \
    && ln -s /usr/bin/grep /usr/bolbok/bin/

USER bolbok

ENTRYPOINT ["/bin/bash", "-r"]
