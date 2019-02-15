FROM ubuntu:18.04

#########################################
### Ubgrade Ubuntu and install essentials
RUN apt-get update && apt-get -y upgrade
RUN apt-get update && apt-get install -y git nano htop gedit

#########################################
## Python 3                                                                                              
RUN apt-get update && apt-get -y install git wget build-essential
RUN apt-get install -y python3 python3-pip
RUN ln -s python3 /usr/bin/python
RUN ln -s pip3 /usr/bin/pip

#########################################
### PyQt5.QtWebEngine
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebengine
ENV PYTHONPATH=/usr/lib/python3/dist-packages

# Singularity
RUN apt-get install -y libarchive-dev
RUN VERSION=2.5.2 && wget https://github.com/singularityware/singularity/releases/download/$VERSION/singularity-$VERSION.tar.gz && tar xvf singularity-$VERSION.tar.gz && cd singularity-$VERSION && ./configure --prefix=/usr/local && make && make install

# # VSCode
RUN apt-get install -y curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
RUN sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
RUN apt-get install -y apt-transport-https && apt-get update && apt-get install -y code

RUN apt-get install sudo
RUN pip install pyyaml

COPY entry.sh /entry.sh
RUN chmod a+x /entry.sh
ENTRYPOINT ["/entry.sh"]