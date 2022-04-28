![Banner](/images/banner.png)
# Bike Assistant – RESTful API Backend and Web Application :bicyclist: :biking_woman:

## Table of Contents
- [Introduction](#introduction)
- [UML Architectural Design](#uml-architectural-design)
- [UML Sequence Diagram](#uml-sequence-diagram)
- [Architectural Description](#architectural-description)
- [Functionalities](#functionalities)
- [API Documentation](#api-documentation)
- [Supplementary Information](#supplementary-information)
- [Project Requirements](#project-requirements)
- [Project Launch](#project-launch)

## Introduction
The “Bike Assistant” project provides a one-stop service for cyclists in Calgary by providing a more convenient, safer, and fun cycling experience. In fact, this User-Friendly software suite allows the user to conveniently take advantage of the city of the Calgary’s cycling infrastructure and amusement places to spend quality free time. It also allows the users to conveniently find the parking lots for bikes near their workplace or other destinations, such as shopping centers or grocery stores. Users can also keep track of their exercise habit by providing them with the information about the estimated Calories they burnt, how much time they spent cycling and the distance they traveled. To allow the parent to keep their children safe, this software suite allows the parents to be aware of the current location, the destination, the estimate time and distance to the destination, of their children, using a user-friendly Web Application.\

“Bike Assistant” is a full-stack software suite consisting of RESTful Web API endpoint, a Relational Database, a NoSQL Database, a User-Friendly Mobile Application, as well as a User-Friendly Web-Based User Interface. As a powerful software suite merits a fine documentation and tutorial, we used different platforms, GitBook, Swagger, and GitHub’s readme, for the documentation. In this software suite we took advantage advances in **Artificial Intelligence (AI)** and used a **Machine Learning (ML)** algorithm, **Q-Learning**, to improve the user’s experience by providing them with most suited amenities based on their location by performing historical and contextual data analysis. For simplification and noise reduction and smoothing of trajectories, we used **Douglas–Peucker** algorithm and **Kalman filtering** technique.

Please visit the other repository [Mobile Application for Bike Assistant](https://github.com/ArashMozhdehi/ENGO-651-Final-Project-Mobile-UI) for the files and descriptions of the Mobile Application. 

## UML Architectural Design
The Figure 1 illustrates the archetectural design sigram of this Software Suite.
<p align="center" width="100%">
    <img width="70%" src="images/software arch.png"> 
    <p align="center" > Figure 1: UML Diagram for Architectural Design</>
</p>
<!-- ![Architectural Design](/images/Picture1.jpg) -->

## UML Sequence Diagram

In Figure 2, you can see the Sequence Diagram of the Web-based Application. For the Sequence Diagram of the Mobile Application

<p align="center" width="100%">
    <img width="100%" src="images/Web UI Sequence Diagram.png"> 
    <p align="center" > Figure 2: UML Sequence Diagram</>
</p>

## Architectural Description
The compentents of this sofeware suite are, as follows:
### 1. Databases
- PostgreSQL database with PostGIS host on Heroku cloud platform to store user’s activity. Figure 3, shows the UML Entity-Relation Diagram.
- **Firebase Real-Time DB**, a NoSQL database, host on Google cloud servers to store the user’s profile and credential. In Figure 4, the data storage model of this Real-Time DB is observable. We used Firebase Real-Time DB, for subscribing and real-time update upon data changes.
- **Firebase Storage** is used for staroage of user's profile images. The storage structure of Firebase Storage allows storing images in file structure instead of in BLOB/CLOB format.

<p align="center" width="100%">
    <img width="100%" src="images/ENGO 651's ERD.png"> 
    <p align="center" > Figure 3: UML Entity-Relation Diagram</>
</p>

<p align="center" width="100%">
    <img width="100%" src="images/Firebase RT DB.png"> 
    <p align="center" > Figure 4: Firebase Real-Time DB's storage model</>
</p>

<p align="center" width="100%">
    <img width="100%" src="images/firebase Storage.png"> 
    <p align="center" > Figure 5: Firebase Storage's storage model</>
</p>

### 2. Backend RESTful API
- Backend RESTful API powered by Flask library of Python.
- Consists of **17 API endpoints**, with over **1,000 lines of code** in Python high-level programming language, that each are explained in detail in GitBook.
- Token assignment is used for secure authorization and authentication when the API is used.
- To prevent **Dictionary, Rainbow, and impade Brute Force attacks**, we used an information security method of Salt concatination and Hasing using SHA256.
### 3. Web Application
- HTML, CSS and JS for asynchronous communication and interactive and responsive front-end.
- Web-UI consist of 12 html pages, 9 CSS stylesheet files. 8 .js script files in JavaScript with over **5,000 lines of code**. 
- It also consists of 18 routes and methods in Python.
- Material UI and Bootstrap 5 for aesthetic an interactive UI design.
- For the **Asynchronous** communication, to improve UX, we used jQuery with **AJAX** without SOAP protocol to take advantage of JSON format instead of XML.
### 4. Mobile Application
- It consist of 27 Java classes with over **15,00 lines of code**.
- It also consists of 27 layout designs with over **9000 lines of code** in XML.
- 
### 5. Others
- Google Map JS SDK for map visualization and a mapping frontend.
- Google Firebase SDK for retrival and storage.
- Google’s Matrix API, Google Place, Google Direction are the other APIs that are used in this web application.
- We used subscription based messagin protocol to keep track on users’ location, bearing, velocity, source, and destination of the Mobile Application users.
- We used **Machine Learning** for best amenity's recommendation.
- jQuery with AJAX without SOAP protocol is used for Async communication.
- For simplification and noise reduction and smoothing of trajectories, we used **Douglas–Peucker** algorithm and **Kalman filtering** technique.
- We used a fromula from "The Compendium of Physical Activities" for Calories burnt calculation.
- [Gitbook](https://arash-mozhdehi.gitbook.io/bike-assistant/) for comprehensive documentation of this project.
- [GitBook](https://arash-mozhdehi.gitbook.io/restful-apis-tutorial/) for API documentation with examples.
- [Swagger](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0) for API documentation with examples.


## Functionalities
### 1. Login

It is a responsive, secure and animated login page. User can login with the credntials that they entered upon registration and password. 

<!-- [![Watch the video](https://i.imgur.com/mtxx7wG.gif)](https://youtu.be/hdLZNZjTaoE) -->

<p align="center" width="100%">
    <img width="90%" src="images/mtxx7wG%5B1%5D.gif"> 
</p>

### 2. Homepage

This aeasthtic dashboard allows access to the other pages.

<!-- ![HomepageWeb](/images/HomepageWeb.PNG) -->
<p align="center" width="100%">
    <img width="90%" src="https://i.imgur.com/1Jjqhkl.gif"> 
</p>

### 3. Logout

The user can logout of the system in two ways, conveinently.

<p align="center" width="100%">
    <img width="90%" src="https://i.imgur.com/uozUOih.gif"> 
</p>

<p align="center" width="100%">
    <img width="90%" src="https://i.imgur.com/fWcMBg5.gif"> 
</p>



### 3. Track Your Bikes
Through receiving the messages for the via MQTT broker it shows the Mobile user's current location. By sending the source, destination, current location of the cyclist, traveling speed, estimated time of arrival, and traveling distance using the Web-Based application parent and loved ones can keep track of the cyclists using MQTT protocol. It shows multiple biker because the application have the ability of multiple login.

<p align="center" width="100%">
    <img width="90%" src="https://i.imgur.com/1Jjqhkl.gif"> 
</p>

### 4. Destinations
![ Destination](/images/Destination.PNG)

It shows different types of destinations within Calgary adopted from Open Data Portal that suitable for cyclists, including the historical sites, city events, bike parks and bike parking lots. 

### 5. Statistical Analysis
![Statistical Analysis](/images/StatisticalAnalysis.PNG)

It shows the historical cycling statistics, including the cycling duration, traveled distance and calories burnt. The duration and travelled distance for the current day and the total of the week are displayed in figures. There are also graphical presentations for the calories burnt and total distance traveled last 7 days. 

### 6. Profile
![EditProfile](/images/EditProfile.PNG)

It shows the user profile, including username, first name, last name, email address, weight, logged in devices and reviews on different places. It also allows user to make changes on the email, weight, password and share their info.

## API Documentation
There are 17 API endpoints built for this project. Please click [here](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0) to see the details with example of each of the API. 

## Supplementary Information
- [Mobile Application Manual]( https://arash-mozhdehi.gitbook.io/bike-assistant/v/mobile-application/)
- [Web-based Application Manual](https://arash-mozhdehi.gitbook.io/bike-assistant/v/web-based-application/)
- [Data Specifications](https://arash-mozhdehi.gitbook.io/bike-assistant/)
- [API Documentation - Swagger](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0)
- [Mobile UI GitHub Repo](https://github.com/ArashMozhdehi/ENGO-651-Final-Project-Mobile-UI)

## Project Requirements and Achievements
The deliverables application satisfies the following requirements for the ENGO 651 course project.
1. "your final project must be sufficiently distinct from the labs in this course, and must be more complex than the labs." : This Mobile Application is far more complex than the lab as it has sophisticated mapping, animation, data collection, data collection, data storage features. (Requirement #1)
2. "must have a mapping front-end": Two thoroughly customized and fully interactive maps, customized for this application's use, with the ability to be intractably customized by the user as well are presented to show the amenities and the locations in the City of Calgary. The user is also provided with the distance and estimated time of reaching the destinations and amenities. (Requirement #2)
3. "must have a RESTful API back-end": The application is connected to the RESTful API back-end, powered by Flask library of python. (Requirement #3)
4. "RESTful API must have authentication": The token connected by the back-end is used for communication with the back-end. (Requirement #4)
5. “API must be documented in detail on GitHub with example uses”: API documentation is prepared on SwaggerHub with details and examples. Please view the GitHub API Documentation section in the readme file. (Requirement #5)
6. "must use at least one open data": This application uses the following data sources for the purpose of mapping and data analysis: (Requirement #6)
   * Open Calgary
     * Parking lot for the bikes
     * Historical sites
     * Ungoing events in the city of Calgary (It only pick the events that are not ended yet)
     * Calgary's historical sites
     * Calgary's benches
     * Calgary's wash rooms
     * Calgary's water fountains
     * Calgary's live traffic incidents
     * Calgary's construction sites
   * Google's APIs
     * Google Maps SDKs
     * Google Directions (For visualizing the bike-friendly route to the destination)
     * Google Distance Matrix (For measuring the distance between the current location of the user and the destination)
     * Google Geocoding (For finding the place based on the Zip Code)
     * Google Geolocation (User's current location)
     * Google Places (For auto-complete)
7. "must use at least one live data set": This mobile application uses the current location of the user and Calgary's live traffic incidents as the live data sources. (Requirement #7)
8. "must perform data analytics using the following data sources": The mobile application performs data analysis on the current location of the user, Calgary's live traffic incidents (another live data source), and construction sites. It sends a notification to the user when he/she approaches those locations. (Requirement #8)
9. "the front-end must be interactive": This mobile application provides a responsive, interactive, user-friendly, aesthetically pleasing, animated through a Android-based UI. (Requirement #9)
10. "solve a problem": The purpose of this Mobile application is to allow the users to find bike-friendly destinations, e.g bike park, and the best bike route for them. It also directs the users to the amenities, e.g. wash room, in the city of Calgary. It also provides safety to the users by giving them heads up about the dangers along the road, e.g. incident sites. (Requirement #10)

## Project Launch
February 2022
