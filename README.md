# EDDN Spark Compose
This is a local Apache Spark cluster with Apache Cassandra database, which can be built quickly and easily using Docker Compose. The focus is on the integration of Elite Dangerous (EDDN) data, which is loaded directly into Cassandra. This makes it possible to run PySpark tests and analyses with Spark directly after initialization.

# Table of Content
[Installation](#Installation)
- [Python 3](##Python-3)
- [Docker](##Docker)
- [Docker Compose](##Docker-Compose)

[Usage](#Usage)
- [Project sections](##Project-sections)
  1. [Load Data from eddb<span></span>.io](###Load-Data-from-eddb<span></span>.io)
  2. [Run Docker-Compose file](###Run-Docker-Compose-file)
  3. [Copy Data to Cassandra](###Copy-Data-to-Cassandra)
  4. [Run PySpark skripts](###Run-pyspark-skripts)
- [Run all in one](##Run-all-in-one)
- [Remove and clean](##Remove-and-clean)

[References](##References)

# Installation
To use the cluster, it is required to install:
1. Python 3
2. Docker
3. Docker Compose 

Docker is needed for the individual components, each of them running in its own container. Docker Compose starts all containers together. And Python 3 is used to load the Elite Dangerous data.

## Python 3
It is recomanded to install the latest version of python 3.

### Linux
Before installing the latest version, check if currently a python 3 installed version on your machine. <br>
To check this, run:

```sh
$ python3 --version
```
Is a version of python 3 installed you can upgrade this to latest version:
```sh
$ sudo apt-get upgrade python3 
```

If you want to install the latest version of python3 you can run: 
```sh
$ sudo apt-get install python3 
```

After the installation you need to check if `pip` (python package manager) is installed along with your python installation:
```sh
$ pip3 -V 
```
If `pip` isn't installed on your machine, run the following command to install it: 
```sh
$ sudo apt install python3-pip
```

### Windows
Download the excecutable installer from https://www.python.org/downloads/windows/ .<br>
After that execute the installer and following the instruction.<br>
Also it possible to install python with Anaconda or with configuration in power shell.

### MacOS

Before installing python make sure that Xcode and Homebrew are installed on your computer.

Isn't that so, then run this in terminal to install Xcode:
```sh
$ xcode-select –install 
```
and this to install Homebrew:
```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" 
```

Now check if a python version is already installed:
```sh
$ python3 --version 
```

Is a version installed you can upgrade this to latest version:
```sh
$ brew update 
```
```sh
$ brew upgrade python3 
```

To install python 3 run this command in your terminal:
```sh
$ brew install python3 
```

After the installation you need to check if `pip` (python package manager) is installed along with your python installation:
```sh
$ pip3 -V 
```

If `pip` isn't installed on your machine, run the following command to install it: 
```sh
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
```
```sh
$ python3 get-pip.py
```

## Docker
### Linux
For deatiled information take a look at the [Docker Documentation](https://docs.docker.com/install/linux/docker-ce/ubuntu/), the first Link in chapter References.

#### Uninstall the old version
Make sure that no outdated Docker version is installed:
```sh
$ sudo apt-get remove docker docker-engine docker.io containerd runc 
```
#### Set up the Repository
Update the `apt` package index:
```sh
$ sudo apt-get update
```
Then install packages to allow `apt` to use a repository over HTTPS:
```sh
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

Now add Docker’s official GPG key:
```sh
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Afterwards check if the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88 was added.
Use the last 8 characters of the fingerprint for searching.
```sh
$ sudo apt-key fingerprint 0EBFCD88
```
At the last use the following command to set up the stable repository.
```sh
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

#### Install the current version of Docker
Update the `apt` package index:
```sh
$ sudo apt-get update 
```

Install the latest version of Docker:
```sh
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Microsoft Windows 

If you haven’t already downloaded the installer (Docker Desktop Installer.exe), you can get it from [download.docker.com](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe).<br>
1. Double-click Docker Desktop for Windows Installer.exe to run the installer. 

2. Follow the install wizard to accept the license, authorize the installer, and proceed with the install. 

3. Click Finish on the setup dialog to complete and launch Docker.


### MacOS 

To install Docker Desktop for Mac download the *Docker.dmg* from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac).<br>
*It is required to sign up on docker hub to download docker for mac.*

1. Double-click *Docker.dmg* to open the installer, then drag Moby the whale to the Applications folder.

2. Double-click *Docker.app* in the Applications folder to start Docker.


## Docker Compose
### Linux

To install docker compose with `curl`, run this command to download the current stable release of Docker Compose:
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 
```

Apply executable permissions to the binary: 
```sh
sudo chmod +x /usr/local/bin/docker-compose 
```

Alternativly you can use `pip` to install docker compose: 
```sh
sudo pip install docker-compose 
```

Test if the installation was successful: 
```sh
$ docker-compose –version 
```
 
### Windows and MacOS 

The desktop version of docker include docker compose.<br> 
So the installation is already done.

# Usage
The execution is devided in single shell scripts. The functionality and benefits are explained in the chapter project section. There is also a shell script which executes all steps together in the correct order. The project is designed for Linux systems, but can be ported with adaptations of the shell scripts for the respective operating system.

## Project sections

Following all steps are described that you need to run in the chapter order to make the project/cluster works.

### Load Data from eddb<span></span>.io
The data that is used comes from the game Elite Dangerous (EDDN) and is provided by the API of the website eddb.io.<br>
With the python script `EDDNClient.py` the data is read by the API and written in JSON format into a .log file (Logs_JSON_EDDN_yyyy-mm-dd).<br> 
The number of downloaded datasets/rows is defined by the argument *--number_of_datasets*.<br>
Afterwards the .log file is transformed with the script `transform_to_csv.py` into a CSV format to make it suitable for Cassandra.

For the execution use the shell script `download_and_transform_data.sh` with the necessary argument:
```sh
$ bash download_and_transform_data.sh -d <Number of datasets that should be downloaded> 
```
or 
```sh
$ bash download_and_transform_data.sh --datasets <Number of datasets that should be downloaded>
```

### Run Docker-Compose file
The cluster can be created after the database has been set up.
To do this, use the shell script `run_docker_compose.sh`. The script expects an argument to specify the number of Spark nodes/slaves. Then Docker Compose is used to build the cluster with the scaled number of Spark nodes.
```sh
$ bash run_docker_compose.sh -n <number of nodes/workers that will be created> 
```
or 
```sh
$ bash run_docker_compose.sh --nodes <number of nodes/workers that will be created> 
```

### Copy Data to Cassandra
After the cluster is initialized, the EDDN data can be loaded into the database. 
Execute the script: 
```sh
$ bash load_data-into_cassandra.sh 
```

This script calls the Cassandra file `copy_data.cql` which creates the keyspace and the table and loads the data from the CSV file.

 
### Run PySpark skripts
The provided PySpark script `eddb_data.py` is just an example. It will select the whole table and write the result into a CSV file in the folder *./compose_cluster/export_data.*

Use this shell script to run PySpark: 
```sh
$ bash exec_pyspark_scripts.sh 
```
In this script you can also insert your own PySpark scripts or replace the existing one to execute them.

**Note**: A pandas function is used to create the CSV. However, this is only useful for small amounts of data, because it loads the data into the RAM before writing. As a result, the RAM runs full if the amount of data is too large. To avoid this you can comment out the following line in the PySpark script `eddb_data.py`:
```python
# df_data.toPandas().to_csv('/tmp/check_cass_data.csv', header=True, encoding='utf8')
```

### Run all in one
To avoid that each step has to be executed separately, a shell script with two arguments can be used:
```sh
$ bash run_all.sh -d <Number of datasets that should be downloaded> -n <number of nodes/workers that will be created>
```
or 
```sh
$ bash run_all.sh --dataset <Number of datasets that should be downloaded> --nodes <number of nodes/workers that will be created>
```
This script executes all steps in the correct order.

**Note**: During the first execution of the script it is possible that the data is not copied and the PySpark script is not executed correctly. This happens because of the initialization time of the Docker Container. If this problem occurs, the error can be fixed by executing the shell script again. Since it is recognized that the cluster already exists when the script is executed again, only the missing steps will be performed. But each time the cluster is executed, the amount of loaded datasets must be specified. Therefore, it is recommended to set this number to a low value when the cluster is executed again. After the cluster has built up, there will be no recurrent complications when running the script again.

### Remove and clean
To remove the cluster with all docker containers and the docker images, use the script:
```sh
$ bash remove_docker_container_images.sh 
```
To delete all created data files, run the script:
```sh
$ bash clean_folders_from_files.sh 
```

## References
These are the references that were used for the creation of the readme.
- https://docs.docker.com/install/linux/docker-ce
- https://docs.docker.com/compose/install/
- https://www.saintlad.com/install-python-3-on-mac/
