# Bike Assistant

## 1. Introduction
“Bike Assistant” mobile application aims to provide an aesthetically pleasing and animated UI for cyclists in Calgary to have one-stop supporting service during their journey. The goal of this project is to provide a more convenient, fun and safer cycling experience for Calgarians.

## 2. Technologies
The following technologies are adopted for this project:
#### 2.1. RESTful API powered by Flask library of Python;
#### 2.2. Backend application developed by Flask library of Python;
#### 2.3. Database design by PostgreSQL RDBMS and hosted in heroku.
#### 2.4 Distance travelled calculation by Haversine Distance library of Python;
#### 2.5 Google Places and Geocoding APIs.

## 3. Functionalities
### 3.1. Start
#### 3.1.1. Splash Screen
Animated introduction of the mobile application.
#### 3.1.2. Internet Connection Checking
Internet connectivity check to ensure user is able to connect the back-end with real-time and semi-real-time API from the open data portal of the city of Calgary.
User will be alerted and asked to activate a Wi-Fi or mobile connection if user is not connected to the Internet.
Use can press exit button to close the application if user does not want to connect to the Internet.
### 3.2. Authentication
#### 3.2.1. Login
It is a secure login system that receives Token from the back-end and stores it in the internal DB. There is secure communication between the flask-based back-end and this Mobile UI. User is required to fill in username and password for login.
#### 3.2.2. Registration
User is required to provide (i) username, (ii) first name, (iii) last name, (iv) password and (v) weight to create an account. Duplicated username is not allowed and the application will check if the user is already existed. Successful registration will be re-directed to login page with username being auto-filled.
### 3.3. Dashboard
User will be asked to allow location permission when reach to the dashboard as the application requires real-time GPS data to provide the best services. User can click on the buttons on the dashboard for different services.
#### 3.3.1. Starts
User can explore the city of Calgary with the mapping front-end. User can select interested type of built-in features or key in (with auto-complete support) a place to find the details of the destination. User can review feedbacks of the selected amenities or type of bike friendly destination. User can get the recommended route to the selected destination. When user is approaching within 100m of a traffic incident or construction project site, a warning notification will be sent to user as a safety alerts.
#### 3.3.2. Amenities
The application supports facilities types of (i) water fountains, (ii) toilets and (iii) bench for searching, routing and providing feedbacks.
#### 3.3.3. Settings
User can perform the following actions: (i) change password and (ii) change weight.
#### 3.3.4. Statistics
User can view the Calories burned Today, last 7 days, and last 30 days with progress bar and bar charts.
#### 3.3.5. Logout
User can logout the session.

## 4. Project Launch
April 2022


