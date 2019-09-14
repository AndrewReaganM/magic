# MAG(i)C Random in Java on Ubuntu 18.04 LTS

## Overview
The Java version of MAG(i)C Random runs on Apache Tomcat, a web server and application server written in Java.

## Prerequisites
* Ubuntu 18.04 LTS server
* Java 1.11.0

## Software Versions
The MAG(i)C Random Number Generator in Python relies on:
* Ubuntu 18.04 LTS
* Java 1.11.0 (OpenJDK)
* Tomcat 9
*

Keep in mind that you may have success running other versions, however it is not guaranteed to work.

## Installing Required Packages from Ubuntu Repositories
To install the required packages, run the following in the terminal of your VM:
```bash
$ apt update
$ sudo apt install default-jdk
```

## Tomcat User and Group for Permissions
To make sure that the installation is secure, Tomcat should run as a non-root user. To create the correct user and group for Tomcat to use, run the following commands:
```bash
$ sudo groupadd tomcat
$ sudo useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat
```

## Installing Tomcat
To install Tomcat, first get the link to the latest Tomcat Binary Distribution Core with a `.tar.gz` file extension. Then run the following bash script:
```bash
$ cd /tmp
$ curl -O <link-to-tar.gz>
```
Next we will install Tomcat to the `/opt/tomcat` directory.
```bash
$ sudo mkdir /opt/tomcat
$ sudo tar xzvf apache-tomcat-9*tar.gz -C /opt/tomcat --strip-components=1
```
## Folder Permissions
We need to give the previously created `tomcat` user permissions to the installation directory.
```bash
$ cd /opt/tomcat
$ sudo chgrp -R tomcat /opt/tomcat
$ sudo chmod -R g+r conf
$ sudo chmod g+x conf
$ sudo chown -R tomcat webapps/ work/ temp/ logs/
```
## Create a System Service File (tomcat.service)
To run Tomcat as a service so that it will run on boot, we need to create a systemd service file. To do this, first find the location of your Java installation, or `JAVA_HOME`. Specifically, you want the one that was installed in the first step, which starts with `/usr/lib/jvm/java...`.
```bash
$ sudo update-java-alternatives -l
```
Copy the whole path of the folder. Now create the service file using `nano`.
```bash
$ sudo nano /etc/systemd/system/tomcat.service
```
Below is the contents of the service file for Tomcat. This template is from DigitalOcean's website.
```
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=<JAVA-LOCATION-REPLACE-THIS>
Environment=CATALINA_PID=/opt/tomcat/temp/tomcat.pid
Environment=CATALINA_HOME=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=tomcat
Group=tomcat
UMask=0007
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```
 Now close the file and select save.

 Now that we have a new service file, we need to reload `systemctl`.

 ```sudo
$ sudo systemctl daemon-reload
$ sudo systemctl start tomcat
$ sudo systemctl status tomcat
 ```
The output of `status` should resemble:
```bash
● tomcat.service - Apache Tomcat Web Application Container
   Loaded: loaded (/etc/systemd/system/tomcat.service; enabled; vendor preset: enabled)
   Active: active (running) since Sat 2019-09-14 18:26:21 UTC; 39min ago
  Process: 1025 ExecStart=/opt/tomcat/bin/startup.sh (code=exited, status=0/SUCCESS)
 Main PID: 1092 (java)
    Tasks: 44 (limit: 4915)
   CGroup: /system.slice/tomcat.service
           └─1092 /usr/lib/jvm/java-1.11.0-openjdk-amd64/bin/java ...
```

## Set up the UFW and Google Cloud VPC Firewall Rules
To allow external devices to communicate with the server, we need to create a couple of firewall rules. These need to be created in two places: The VM's built in firewall, and in the Google Cloud console under "VPC Network > Firewall rules".

To allow external access on the VM side, simply open the port with the following command:
```bash
$ sudo ufw allow 8080
```

To allow using GCP, see the documentation (here)[https://cloud.google.com/vpc/docs/using-firewalls], and use the following info:
```
name: <something-descriptive>
network: default
logs: off
priority: 1000 # Default
direction: ingress
action on match: allow
Targets: Specified target tags
Target tags: "tomcat-admin"
Source filter: IP ranges
Source IP ranges: 0.0.0.0/0 # All networks and IPs
Second source filter: none
Protocols and ports: Specified protocols and ports
  tcp: 8080
```
Then, click save.

Now, in the Compute Engine Instance dashboard, select your instance and edit it. Under Network Tags, add "tomcat-admin" and click save.


Now, try accesing the Tomcat homepage using the following link format.
```bash
http://server-ip-domain:8080
```

If the Tomcat homepage did not load, you need to troubleshoot before proceeding. If it did load, it is time to enable the `tomcat.service` file to run at boot:
```bash
$ sudo systemctl enable tomcat
```
















## Troubleshooting
Please look in the following locations for error/connection logs:
```bash
$ sudo command wow
```

##
