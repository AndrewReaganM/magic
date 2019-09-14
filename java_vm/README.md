# MAG(i)C Random in Java on Ubuntu 18.04 LTS
This is a simple overview of how a functioning implementation of the random number generator was achieved using Java. Most of the guidance on how to do this was from the DigitalOcean article on how to set up Tomcat on Ubuntu 18.04 LTS, located here: [DigitalOcean and Flask](https://www.digitalocean.com/community/tutorials/install-tomcat-9-ubuntu-1804)

## Prerequisites
* Ubuntu 18.04 LTS server

## Software Versions
The MAG(i)C Random Number Generator in Python relies on:
* Ubuntu 18.04 LTS
* Java 1.11.0 (OpenJDK)
* Tomcat 9

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
To install Tomcat, first get the link to the latest Tomcat Binary Distribution Core with a `.tar.gz` file extension. Then run the following in your terminal:
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
We need to give the previously created `tomcat` user permissions to the installation directory. Do this by running the following commands:
```bash
$ cd /opt/tomcat
$ sudo chgrp -R tomcat /opt/tomcat
$ sudo chmod -R g+r conf
$ sudo chmod g+x conf
$ sudo chown -R tomcat webapps/ work/ temp/ logs/
```
## Create a System Service File (tomcat.service)
To add Tomcat as a service so that it will start on boot, we need to create a systemd service file. To do this, first find the location of your Java installation, or `JAVA_HOME`. Specifically, you want the one that was installed in the first step whose path starts with `/usr/lib/jvm/...`.
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

 Now that we have a new service file, we need to reload `systemctl` and start the `tomcat` service.

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
To allow external devices to communicate with the server, we need to create a couple of firewall rules. These need to be created in two places: The VM's built in firewall, and the Google Cloud console under "VPC Network > Firewall rules".

To allow external access on the VM side, simply open the port with the following command:
```bash
$ sudo ufw allow 8080
```

To allow using GCP, see the documentation [here](https://cloud.google.com/vpc/docs/using-firewalls), and use the following info, saving the rule after completion:
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

Now, in the Compute Engine Instance dashboard, select the instance used for Tomcat and edit it. Under Network Tags, add "tomcat-admin" and click save.


Now, try accesing the Tomcat homepage using the following link format:
```bash
http://server-ip-domain:8080
```

If the Tomcat homepage did not load, you need to troubleshoot before proceeding. If it did load, it is time to enable the `tomcat.service` file to run at boot:
```bash
$ sudo systemctl enable tomcat
```

## Set up Tomcat Web Interface
To manage our tomcat installation, we must create a user for the web interface:
```bash
$ sudo nano /opt/tomcat/conf/tomcat-users.xml
```
Add the following line in between the `<tomcat-users>` tags:
```
<user username="admin" password="password" roles="manager-gui,admin-gui"/>
```
Make sure to set a username and password that is secure. Note that the username `admin` is a locked username, so you must use a different one.

To allow remote administration of the Tomcat server edit both of the following files as indicated below:
```bash
$ sudo nano /opt/tomcat/webapps/manager/META-INF/context.xml

# and after

$ sudo nano /opt/tomcat/webapps/host-manager/META-INF/context.xml
```

Edit the files by commenting out the IP restriction as follows:
```
# Example provided by DigitalOcean
<Context antiResourceLocking="false" privileged="true" >
  <!--<Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
</Context>
```

Now that both of those files have been changed, restart Tomcat.
```bash
$ sudo systemctl restart tomcat
```

Now, try logging into the server by accessing the homepage, selecting "Manager App" and using the username and password set previously:
```bash
http://server-ip-domain:8080
```

## Creating the WebApp
The Google AppEngine plugin for Eclipse, while meant for working with appengine, makes it convenient to develop for TomCat as well.

### Installing Google Cloud SDK
To install the Cloud SDK, using [Google's Documentation](https://cloud.google.com/sdk/docs/).

The SDK will need java appengine features installed
  Run the command `gcloud components install app-engine-java` from the Google Cloud SDK Shell

### Setting up Eclipse
This guide assumes you are using a new install of Eclipse 2019-06 for Java Developers. This section is the same as the `Setting up Eclipse` section for the Java AppEngine. If you have already followed those steps, you can skip this section.

Eclipse needs addons installed to support web development. Do this by going to Help -> Install New Software
For the `Work with:` input, select "2019-06 - http://download.eclipse.org/releases/2019-06"
Expand "Web, XML, Java EE, and OSGi Enterprise Development"
Select the following 3 packages:
  `Eclipse Java EE Developoer Tools`
  `Eclipse Java Web Developer Tools`
  `Eclipse Web Developer Tools`
Click `Finish`, wait for the packages to install, then restart eclipse

Install the Google Cloud Tools for Eclipse: [Instructions](https://cloud.google.com/eclipse/docs/quickstart#installing)
Restart eclipse after installation
  
### Creating the Project
A sample Hello World project can be created by following the [instructions](https://cloud.google.com/eclipse/docs/creating-new-webapp)
Further development steps can be found in the pages that follow.

Create a new App Engine Standard Project
  Select the `Google Cloud Engine` contextual menu and the choose `Create New Project -> Google App Engine Standard Java Project...`

Clean default files out of project
  Delete `src/test/java/HelloAppEngineTest.java`
  Delete `src/test/java/MockHttpServletResponse.java`
  Delete `src/main/java/HelloAppEngine.java`
  Delete `src/main/webapp/index.html`
  Open `src/main/webapp/WEB-INF/web.xml`
    Remove `welcome-file-list` and save the file

Create a new servlet
  Right click `src/main/java` and choose `New -> Other...`
  From the menu, choose `Web -> Servlet`
  Give the servlet a name and click `Finish`
  
Clean up the new servlet
  Delete the constructor
  Delete doPost(...)
  
Configure the servlet
  Change the line `@WebServlet("/YourServletName")` to `@WebServlet("/")`
  Make doGet(...) write a random number to response
```Java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
  response.setContentType("text/plain");
  response.setCharacterEncoding("UTF-8");

  Random rand = new Random();
  response.getWriter().print(rand.nextInt(999999)+1);
}
```

Create the .WAR file
  Once the webapp is finished and ready to be deployed, right click on the project and select `Export -> WAR file`
  Select your project from the list if it is not already selected
  Choose where you want to export the project to
  Uncheck the box `Optimize for a specific runtime`

## Uploading and Configuring the WebApp
Access the TomCat Manager at http://<your_server>/manager/html
  You will be asked to login, use the credentials you specified in the [Set up Tomcat Web Interface](#set-up-tomcat-web-interface)

Find the section labeled `WAR file to deploy`
  Browse for the [WAR](https://github.com/AndrewReaganM/magic/blob/master/java_vm/java_vm.war)
  Click `Deploy`
  
You webapp will now be accessible through the url http://<your_server>/<web_app_name>
  You can also find a link in the `Applications` table
  
### Run the WebApp at the Root
We want the webapp to be accessible at http://<your_server> instead of http://<your_server>/<web_app_name>

Remove the homepage
  Find the application with the path `/` in the Applications table
  Select Undeploy for that record
  
Set your application to run at `/`
  SSH into the server and access the file `/opt/tomcat/conf/server.xml`
  Add the following line at the end of `<Host>` tags
  ```
  <Context path="" docBase="<your_web_app_name>"></Context>
  ```

Restart the VM and your webapp will now be accessible at http://<your_server>/

## Troubleshooting
Please see the Tomcat documentation for troubleshooting steps.
