FROM amazonlinux:latest

RUN yum -y update && yum clean metadata && \
yum -y install \ 
  gcc \
  gcc-c++ \
  freetype-devel \
  yum-utils \
  findutils \
  openssl-devel \
  groupinstall \
  development \
  tar.x86_64 \
  xz \
  make

RUN yum-builddep python3

# Install python3.10.4
RUN curl https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tar.xz | tar -xJ \
	&& cd Python-3.10.4 \
	&& ./configure --prefix=/usr/local --enable-shared \
	&& make && make install \
	&& cd .. && rm -rf Python-3.10.4
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH


# Install Python modules to a /tmp/vendored directory that we will zip
# up for deployment to Lambda.
# - We force a build of numpy from source to get a lighter distribution (save ~40Mb).
# - To skip GDAL compilation we use binary rasterio wheels from PyPI.
# - The `[s3]` option will install rasterio + boto3 to enable AWS S3 files support.
# - We use --pre option to force the install of rasterio alpha 1.0 version


RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -t /tmp/vendored --no-binary numpy --pre rasterio
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -t /tmp/vendored --no-binary
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -t /tmp/vendored --no-binary
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pandas -t /tmp/vendored


# Echo the estimated size of the package
# RUN du -sh /tmp/vendored
# Create the zip file
RUN cd /tmp/vendored && zip -r9q /tmp/package.zip *
# RUN du -sh /tmp/package.zip