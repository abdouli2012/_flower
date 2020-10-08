FROM python:3.7.9-slim-stretch

RUN apt-get update
RUN apt-get install -y openssh-server screen
RUN mkdir /var/run/sshd

RUN echo 'root:root' | chpasswd

RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh

ARG SSH_PUBLIC_KEY
RUN echo $SSH_PUBLIC_KEY > /root/.ssh/authorized_keys

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /root

RUN pip install tensorflow-cpu==2.2.0 torch==1.6.0 numpy==1.18.3
COPY dist/flwr-0.8.0-py3-none-any.whl flwr-0.8.0-py3-none-any.whl
RUN python -m pip install --no-cache-dir 'flwr-0.8.0-py3-none-any.whl[examples-pytorch,examples-tensorflow,http-logger,baseline,ops]' && \
    rm flwr-0.8.0-py3-none-any.whl

RUN python3.7 -m flwr_experimental.baseline.tf_fashion_mnist.download
RUN python3.7 -m flwr_experimental.baseline.tf_cifar.download
RUN python3.7 -m flwr_experimental.baseline.torch_cifar.download

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
