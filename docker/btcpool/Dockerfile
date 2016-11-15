#
# Dockerfile
#
# @author hyperwangee@gmail.com
# @copyright haobtc.com
# @since 2016-09-21
#

FROM phusion/baseimage:0.9.19
MAINTAINER HyperWang <hyperwangee@gmail.com>

ENV HOME /root

# use aliyun source
ADD docker/btcpool/sources-aliyun.com.list /etc/apt/sources.list

# apt-get
RUN apt-get update
RUN apt-get install -y build-essential autotools-dev libtool autoconf automake pkg-config cmake wget
RUN apt-get update
RUN apt-get install -y openssl libssl-dev libcurl4-openssl-dev libconfig++-dev libboost-all-dev libmysqlclient-dev --fix-missing

RUN mkdir -p /root/source
WORKDIR /root/source

# zmq-v4.1.5
RUN wget https://github.com/zeromq/zeromq4-1/releases/download/v4.1.5/zeromq-4.1.5.tar.gz
RUN tar zxvf zeromq-4.1.5.tar.gz \
    && cd zeromq-4.1.5 \
    && ./autogen.sh \
    && ./configure \
    && make
RUN cd zeromq-4.1.5 \ 
    && make install \
    && ldconfig

# glog-v0.3.4
RUN wget https://github.com/google/glog/archive/v0.3.4.tar.gz
RUN tar zxvf v0.3.4.tar.gz
RUN cd glog-0.3.4 \
    && ./configure && make && make install

# librdkafka-v0.9.1
RUN apt-get install -y zlib1g zlib1g-dev
RUN wget https://github.com/edenhill/librdkafka/archive/0.9.1.tar.gz
RUN tar zxvf 0.9.1.tar.gz
RUN cd librdkafka-0.9.1 \
    && ./configure && make && make install

# libevent
RUN wget https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz
RUN tar zxvf libevent-2.0.22-stable.tar.gz
RUN cd libevent-2.0.22-stable \
    && ./configure \
    && make \
    && make install

### btcpool
#RUN apt-get install -y git
#RUN mkdir -p /work \
#    && cd /work \
#    && git clone https://github.com/btccom/btcpool.git
#RUN cd /work/btcpool \
#    && mkdir build \
#    && cd build \
#    && cmake -DCMAKE_BUILD_TYPE=Release .. \
#    && make
#RUN cd /work/btcpool/build \
#    && cp gbtmaker blkmaker jobmaker /usr/local/bin \
#    && cp poolwatcher sharelogger sserver /usr/local/bin \
#    && cp slparser statshttpd /usr/local/bin 

#RUN apt-get install -y git
RUN mkdir -p /work/btcpool
ADD src /work/btcpool/src
ADD test /work/btcpool/test
ADD cmake /work/btcpool/cmake
ADD CMakeLists.txt /work/btcpool/CMakeLists.txt
RUN cd /work/btcpool \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release .. \
    && make
RUN cd /work/btcpool/build \
    && cp gbtmaker blkmaker jobmaker /usr/local/bin \
    && cp poolwatcher sharelogger sserver /usr/local/bin \
    && cp slparser statshttpd /usr/local/bin 

# script for running components
RUN mkdir -p /opt/btcpool/conf
RUN mkdir -p /opt/btcpool/log
WORKDIR /root/
ADD docker/btcpool/run.py run.py
ENTRYPOINT ["python", "run.py"]
CMD ["-h"]
