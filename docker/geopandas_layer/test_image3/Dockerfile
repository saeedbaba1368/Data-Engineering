FROM amazonlinux:latest

USER root
RUN mkdir -p $APP_DIR/lib
RUN yum update -y
RUN yum install wget -y
RUN yum install pip -y
RUN yum install bzip2-devel -y
RUN yum install -y xz-devel
RUN yum -y groupinstall development
RUN yum -y install zlib-devel
RUN yum -y install openssl-devel



RUN wget https://github.com/openssl/openssl/archive/OpenSSL_1_0_2l.tar.gz
RUN tar -zxvf OpenSSL_1_0_2l.tar.gz 
WORKDIR "openssl-OpenSSL_1_0_2l/"
RUN ./config shared
RUN make
RUN make install
WORKDIR /
RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
RUN tar xJf Python-3.6.3.tar.xz
WORKDIR Python-3.6.3
RUN ./configure
RUN make
RUN make install
WORKDIR /
RUN rm Python-3.6.3.tar.xz
RUN rm -rf Python-3.6.3
RUN pip install --upgrade virtualenv
RUN virtualenv -p python3 MYVENV
ENV PATH /MYVENV/bin:$PATH

COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt --target lib/
ADD lib/. /opt/app/lib/