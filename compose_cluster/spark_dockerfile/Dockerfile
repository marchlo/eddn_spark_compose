FROM python:3.7

# Add jessie backport repo to soruces for java 8
COPY java-8-deb-repository.list /etc/apt/sources.list.d/

# Install all debian packages
RUN apt-get update && apt-get install -y \
	vim net-tools \
	openjdk-8-jdk \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy all source files to the container's working directory
COPY . /app/
WORKDIR /app/

# Download the spark binaries tar file, extract it and then delete it
RUN (mkdir spark && \
	wget http://ftp-stud.hs-esslingen.de/pub/Mirrors/ftp.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz && \	
	tar zxf spark-2.4.3-bin-hadoop2.7.tgz -C spark --strip-components=1 && \
	rm spark-2.4.3-bin-hadoop2.7.tgz)

RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install pyspark


CMD ["/app/entrypoint.sh"]