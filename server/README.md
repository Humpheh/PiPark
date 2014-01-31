# PiPark Car Parking Sensor
**Installation Instructions and Usage** (Version 1)

---

## Server Setup
These are the instructions for installing the server software of which the *Raspberry Pi* car parking sensors will send data to. The software provides a UI for viewing available car parking spaces which can be viewed from a web browser.

For the purposes of this guide, we will be setting up the server on a test environment using the XAMPP program to host a server on a computer. The XAMPP program can be downloaded from [the XAMPP website](http://www.apachefriends.org/index.html).

### **Step 1** - Get Software
Once the server software has been installed, download the files from the ```/server/``` directory of the repository. Place the folder in the root of the server directory. 

*For XAMPP setup, this directory is usually called ```htdocs``` and is found in the install directory. Also ensure that the software is running at this point.*

### **Step 2** - Create Database
The next step is to create a database on the server using the script found in ```/admin/db.sql```. Make note of the database name and the login details.

*For XAMPP setup, you can create the database by going to ```http://localhost/phpmyadmin/``` and creating a database. You can paste the script found in ```/admin/db.sql``` into the SQL tab at the top of the page to create the tables.*

### **Step 3** - Configure Website
When the database is created, you need to open the file ```/config.php``` located in the root directory of the website. Here you must change the values of DB_HOST, DB_USER, DB_PASS and DB_DATABASE to match the details you used in the previous step. (*For XAMPP, the default USER and PASS are "root" and "" respectively.*)

In this file, also change the variables URL_BASE, PI_PASSWORD and TITLE. 
* **URL_BASE** is the base URL to access the website on the server. 
* **PI_PASSWORD** is the password the pi's will require to update data on the server.
* **TITLE** is the title of the website used in the website UI.

### **Step 4** - Finish
The server should now be setup correctly. Heading over to the URL (*http://localhost/[DIRECTORY IN HTDOCS]/ for XAMPP*) should display the home page of the site.

---

## Site Usage
### Managing Car Parks
To add a new car park, click on the 'Park Management' button in the navigation bar. This page will display the current registered on the database. To add a new car park, complete the form at the bottom of the page. Car parks may also be edited or deleted using the buttons to the right.

**NOTE:** The ID on the left in the rows is the *unique* identifier for that car park. This number will be needed when registering the pi's on the database during setup.

### API
There is a basic API JSON interface built into the website. This can be accessed at ```/api.php``` in the server root. It gives some basic information about the car parks in a JSON format. This could then be used for future applications, such as possibly having sat nav's communicating with this data.
