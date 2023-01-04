FROM lambci/lambda:build-python3.7

ENV \
 POSTGRES_VER=11.4 \
 PSYCOPG_VER=2.8.3 \
 PSYCOPY_MAJ_VER=2.8 \
 PSYCOPG_VER_PATH=PSYCOPG-2-8 \
 PYTHON_VER=3.7

RUN yum install -y wget tar postgresql-devel
#RUN yum install ca-certificates

#setup output dir for library extraction
RUN mkdir -p /var/output

# PSYCOPG2
WORKDIR /var/psycopg

RUN wget -nv https://ftp.postgresql.org/pub/source/v${POSTGRES_VER}/postgresql-${POSTGRES_VER}.tar.gz --no-check-certificate
RUN tar -zxf postgresql-${POSTGRES_VER}.tar.gz
RUN wget -nv http://initd.org/psycopg/tarballs/${PSYCOPG_VER_PATH}/psycopg2-${PSYCOPG_VER}.tar.gz --no-check-certificate
RUN tar -zxf psycopg2-${PSYCOPG_VER}.tar.gz

# build postgres with ssl
#RUN cd postgresql-${POSTGRES_VER} && \
#./configure --prefix /var/psycopg/postgresql-${POSTGRES_VER} --without-readline --without-zlib --with-openssl && \
#make && \
#make install

# build without ssl
RUN cd postgresql-${POSTGRES_VER} && \
./configure --prefix /var/psycopg/postgresql-${POSTGRES_VER} --without-readline --without-zlib && \
make && \
make install

# build psycopg2
# need to replace some values in the config file so they point to postgres install and enable ssl
RUN ls
RUN cd psycopg2-${PSYCOPG_VER} && \
sed -ie "s/pg_config =/pg_config = \/var\/psycopg\/postgresql-$POSTGRES_VER\/bin\/pg_config/g" setup.cfg && \
sed -i 's/static_libpq = 0/static_libpq = 1/g' setup.cfg 

# ADD && \ to end of previous RUN if configuring for SSL so the next command is part of prior
#sed -i 's/libraries =/libraries = ssl crypto/g' setup.cfg

RUN cat psycopg2-${PSYCOPG_VER}/setup.cfg
RUN ls /var/psycopg/postgresql-${POSTGRES_VER}
RUN cd psycopg2-${PSYCOPG_VER} && python setup.py build

# copy compiled library to output to deliever to host
RUN ls
RUN cp -r /var/psycopg/psycopg2-${PSYCOPG_VER}/build/lib.linux-x86_64-${PYTHON_VER}/psycopg2 /var/output