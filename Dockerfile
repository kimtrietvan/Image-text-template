FROM ubuntu:23.10

# Install python/pip
RUN apt --assume-yes update
RUN apt --assume-yes upgrade
RUN apt --assume-yes install curl
RUN apt --assume-yes install git
RUN apt --assume-yes install software-properties-common
RUN apt --assume-yes install python3.11
RUN apt --assume-yes install python3-pip
# Install Nodejs
RUN apt install -y nodejs npm
# Install U2net
RUN mkdir /root/.u2net
RUN curl -o /root/.u2net/u2net.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx

WORKDIR /root/app

COPY . .
RUN pip install pip==22.3.1 --break-system-packages
RUN pip3 install -r requirements.txt
# RUN pip3 install numpy==1.14.2
# RUN pip3 install onnx
# RUN pip3 install onnxruntime
# RUN pip3 install rembg[cli]
RUN cd node-file-manager && npm install

CMD ["sh", "/root/app/endpoint.sh"]