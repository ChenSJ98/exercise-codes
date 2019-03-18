# <center> DISTRIBUTED AND CLOUD COMPUTING</center>

<center><bold> LAB ASSIGNMENT 1</bold></center>

Student Name: Shijie Chen
Student ID: 11612028
Student E-mail: Chrischen369@outlook.com

## Design

### Module Design

The module includes 3 parts:

* Application: the RMI Server and RMI Client
* Dao: Data access object which handles communication with a remote MySQL database
* RmiUtility: The implementation of RMI methods

The credentials are encrypted using BCrypt algorithm implemented by Damien Miller. (https://www.mindrot.org/projects/jBCrypt/)

### Class Design

* UML:
* 

## Problems

The major design decisions:

* Inspired by the RMI documentation and the project structure of Springboot framework, I decide to split the project into frontend (UI) and backend (data processing and the use of database).

Problems encountered:

* missing jdbc driver; solution: add the .jar file to the project folder and add it to search path in Intellij Idea

## Running Result

Server:

![1552298807948](C:\Users\SHIJIE~1\AppData\Local\Temp\1552298807948.png)

Client:

![1552298966256](C:\Users\SHIJIE~1\AppData\Local\Temp\1552298966256.png)

Database:

![1552299056272](C:\Users\SHIJIE~1\AppData\Local\Temp\1552299056272.png)

The password is encrypted.