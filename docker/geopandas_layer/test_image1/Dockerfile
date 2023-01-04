FROM amazonlinux:latest

RUN yum -y update && yum clean metadata && \
yum -y install \
  wget \
  tar \
  gzip \
  make \
  gcc \
  openssl-devel \
  bzip2-devel \
  libffi-devel \
  sqlite-devel \
  zip \
  git \
  which \
  gcc \
  gcc-c++ \
  freetype-devel \
  findutils \
  groupinstall \
  development \
  gcc-gfortran \
  make

WORKDIR /opt

RUN wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
RUN tar xzf Python-3.9.7.tgz

WORKDIR /opt/Python-3.9.7

RUN ./configure --enable-optimizations
RUN make altinstall

WORKDIR /

RUN rm -rf /opt/Python-3.9.7*

RUN ln -s $(which python3.9) /usr/local/bin/python3
RUN python3 -m pip install -U pip

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip setuptools

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  rasterio[s3] -t /tmp/vendored --no-binary numpy --pre rasterio
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  geopandas[s3] -t /tmp/vendored --no-binary
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  rasterstats[s3] -t /tmp/vendored --no-binary
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  pandas -t /tmp/vendored
RUN cd /tmp/vendored && zip -r9q /tmp/package.zip *