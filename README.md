![Banner](/images/banner.png)
# Bike Assistant :bicyclist: :biking_woman:

## Table of Contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Functionalities](#functionalities)
- [API Documentation](#api-documentation)
- [Supplementary Information](#supplementary-information)
- [Project Launch](#project-launch)

## Introduction
“Bike Assistant” is a software suite aims to provide an aesthetically pleasing and animated UI for cyclists in Calgary to have one-stop supporting service during their journey. The goal of this project is to provide a more convenient, fun and safer cycling experience for Calgarians. “Bike Assistant” consists of an android mobile app and an interactive web map app. This file describes the technologies and technical details applied in this project as well as the functionalities of the web map app. Please refer to [another repo](https://github.com/ArashMozhdehi/ENGO-651-Final-Project-Mobile-UI) of this project for the mobile app details. [Requirement #1 and #10 – apply lab materials in a more complex way and solve a problem]

## Technologies
The following technologies are adopted for this project:
### 1. Database
- PostgreSQL with PostGIS database host on Heroku cloud platform to store user’s activity;
- Firebase real-time DB as NoSQL database host on Google cloud servers to store the user’s profile and credential;
- SHA256 to store the user’s password in hash;
### 2. Backend API
- Backend RESTful API powered by Flask library of Python; [Requirement #3 – RESTful API backend]
- Token assignment and token-based authorization and authentication with SHA256;
### 3. Web Application
- HTML, CSS and JS for asynchronous communication and interactive and responsive front-end; [Requirement #9 – interactive frontend]
- Material UI and Bootstrap 5 for UI design;
### 4. Mobile Application
- Android Studio IDE for Android-based application development;
### 5. Others
- Google Map SDK for map visualization and a mapping frontend;
- Google’s Matrix API and Google Direction (contextual geospatial data) for data analytics;
- MQTT protocol from broker to keep track on users’ location, bearing, velocity, source, and destination of the Mobile Application users
- Artificial Intelligence for best place recommendation; 
- jQuery with AJAX without SOAP protocol for Async communication;
- Formula from "The Compendium of Physical Activities" for Calories burnt calculation;
- [Gitbook](https://arash-mozhdehi.gitbook.io/bike-assistant/v/web-based-application/) for comprehensive documentation of this project;
- [Swagger](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0) for API documentation with examples


## Functionalities
### 1. Login
![LoginWeb](/images/LoginWeb.PNG)

It is a responsive, secure and animated login page. User can login with username and password. [Requirement #4 – authentication]
### 2. Homepage
![HomepageWeb](/images/HomepageWeb.PNG)

There is a menu bar on the right hand side for selecting different applications.

### 3. Track Your Bikes
![ FindYourBike](/images/FindYourBike.PNG)

It supports tracking of a bike by showing the starting point, destination, bike current location and the recommended route. [Requirement #7 and #8 – using live data set and data analytics using real-time data of IoT device]

### 4. Destinations
![ Destination](/images/Destination.PNG)

It shows different types of destinations within Calgary adopted from Open Data Portal that suitable for cyclists, including the historical sites, city events, bike parks and bike parking lots. [Requirement #6 and #7– open data and frequent update data]

### 5. Statistical Analysis
![Statistical Analysis](/images/StatisticalAnalysis.PNG)

It shows the historical cycling statistics, including the cycling duration, traveled distance and calories burnt. The duration and travelled distance for the current day and the total of the week are displayed in figures. There are also graphical presentations for the calories burnt and total distance traveled last 7 days. [Requirement #8 – data analytics using historical data of IoT device]

### 6. Profile
![EditProfile](/images/EditProfile.PNG)

It shows the user profile, including username, first name, last name, email address, weight, logged in devices and reviews on different places. It also allows user to make changes on the email, weight, password and write something about me.

## API Documentation
There are 17 API endpoints built for this project. Please click [here](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0) to see the details with example of each of the API. [Requirement #5 – API documentation in details]

## Supplementary Information
- [Mobile Application Manual]( https://arash-mozhdehi.gitbook.io/bike-assistant/v/mobile-application/)
- [Web-based Application Manual](https://arash-mozhdehi.gitbook.io/bike-assistant/v/web-based-application/)
- [Data Specifications](https://arash-mozhdehi.gitbook.io/bike-assistant/)
- [API Documentation - Swagger](https://app.swaggerhub.com/apis-docs/uofcengo/BikeAssistance/1.0.0)
- [Mobile UI GitHub Repo](https://github.com/ArashMozhdehi/ENGO-651-Final-Project-Mobile-UI)

## Project Launch
April 2022
