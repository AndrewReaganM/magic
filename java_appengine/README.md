# MAG(i)C Random on Google AppEngine

## Overview
A working version of this software can be found at
```url
https://software-engineering-250801.appspot.com/
```

## Prerequisites

## Software Versions
The MAG(i)C Random Number Generator in Java

## Developing/Deploying Java for AppEngine
The Google AppEngine plugin for Eclipse allows you to create appengine projects, test on a local appengine, and deploy to the cloud.

### Installing Google Cloud SDK
To install the Cloud SDK, using [Google's Documentation](https://cloud.google.com/sdk/docs/).

The SDK will need java appengine features installed
  * Run the command `gcloud components install app-engine-java` from the Google Cloud SDK Shell

### Setting up Eclipse
This guide assumes you are using a new install of Eclipse 2019-06 for Java Developers. This section is the same as the `Setting up Eclipse` section for the Java VM. If you have already followed those steps, you can skip this section.

Eclipse needs addons installed to support web development. Do this by going to Help -> Install New Software
For the `Work with:` input, select "2019-06 - http://download.eclipse.org/releases/2019-06"
Expand "Web, XML, Java EE, and OSGi Enterprise Development"
Select the following 3 packages:
  * `Eclipse Java EE Developoer Tools`
  * `Eclipse Java Web Developer Tools`
  * `Eclipse Web Developer Tools`
Click `Finish`, wait for the packages to install, then restart eclipse

Install the Google Cloud Tools for Eclipse: [Instructions](https://cloud.google.com/eclipse/docs/quickstart#installing)
Restart eclipse after installation
  
### Creating the Project
Create a new App Engine Standard Project
  * Select the `Google Cloud Engine` contextual menu and the choose `Create New Project -> Google App Engine Standard Java Project...`

Clean default files out of project
  * Delete `src/test/java/HelloAppEngineTest.java`
  * Delete `src/test/java/MockHttpServletResponse.java`
  * Delete `src/main/java/HelloAppEngine.java`
  * Delete `src/main/webapp/index.html`
  * Open `src/main/webapp/WEB-INF/web.xml`
    * Remove `welcome-file-list` and save the file

Create a new servlet
  * Right click `src/main/java` and choose `New -> Other...`
  * From the menu, choose `Web -> Servlet`
  * Give the servlet a name and click `Finish`
  
Clean up the new servlet
  * Delete the constructor
  * Delete doPost(...)
  
Configure the servlet
  * Change the line `@WebServlet("/YourServletName")` to `@WebServlet("/")`
  * Make doGet(...) write a random number to response
```Java
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
  response.setContentType("text/plain");
  response.setCharacterEncoding("UTF-8");

  Random rand = new Random();
  response.getWriter().print(rand.nextInt(999999)+1);
}
```

### Deploying to AppEngine
Follow the [instructions](https://cloud.google.com/eclipse/docs/deploying) for deploying to a standard appengine

For deploying our Java AppEngine project, clone our repository and import the java_appengine folder as a project, then follow the steps linked above.
