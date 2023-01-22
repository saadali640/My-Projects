# YOUR PROJECT TITLE: waves
#### Video Demo:  <URL https://youtu.be/2lomq_T7ypc>
#### Description: Social Media WebApp

This is a describtion of my CS50's final project "waves",
"waves" is a social network WebApp that allows users to create an account which will enable them to
 * Set frofile picture using URL.
 * Set frofile background picture using URL.
 * Set a profile bio.
 * Create posts.
 * See each other's posts.
 * Comment on each other's posts.
 * Like each other's posts.

This project was created using
 * python
 * HTML
 * CSS
 * jinja
 * SQL
 * flask

Files on this project are static, templates, app.py and project.db.
In the static file you will find
 * "pic.jpg" which is the background image of the site.
 * "styles.css" which contains the css for the navbar, buttons, body ect...

In the templates file you will find
 * "layout.html" which contains the HTML and jinja that will serve as the structure of the site which will be extended to the rest of the templates using jinja.
 * "index.html" which contains the HTML and jinja for the home page displaying all posts from users in "waves" community.
 * "login.html" which contains the form for allowing registered users to login.
 * "register.html" which contains the form for registering new users.
 * "profile.html" this template shows the users profile containing the user's posts, profile picture, background picture, username, bio.
    On this page The user is able to
      - set background picture
      - set profile picture
      - set bio
      - create new post
      - view all posts posted by the user

 * "oup.html" this template shows other users profile containing user's background picture, profile picture, username, bio and all posts posted by the user.
 * "view.html" this template will display after clicking on a post showing the comments on that post and allowing the user to comment, like and unlike the post.

In the app.py file you will find the backend python code for this project.
libraries user in this project are
 * os
 * flask import Flask, flash, redirect, render_template, request, session, url_for
 * tempfile import mkdtemp
 * werkzeug.security import check_password_hash, generate_password_hash
 * datetime
 * flask_session import Session
 * cs50 import SQL
 * functools import wraps

Functions in app.py are
 * login_required(f)
  - To redirect the user to the login page when trying to access the site without loging in
 * index()
  - To query the database selecting all posts posted by other users then sending and rendering the results to the index.html template
 * profile()
  - To query the database selecting the user's data then sending and rendering the results to the profile.html template
  - On POST request method the function sends a boolean value to the template to either show the "edit profile" or "create post" options depending on the value posted to the functio
 * edit()
  - When editing the profile info the values are posted to this fuction to be saved by updating the user's info in the database
 * newpost()
  - When creating a new post the values are sent to this fuction to be inserted into the database
 * oup(id)
  - This function gets the id number of a user when clicking on their username on a post then selecting all their info and posts posted by them to show it in a page representing their profile page without giving other users the ability to edit any of its content
 * search()
  - This function allow users to search the platform for other users by username
 * comment(id)
  - When submitting a comment this function inserts comment into database linking it to the post by post_id
 * view(id)
  - When clicking on a post this function shows the comment and allow users the comment and like and dislike the post
 * add(id)
  - Using the post's id this function adds the user's id and post's id to the database in the liked table when users like the post
 * remove(id)
  - Using the post's id this function removes the user's id and post's id from the database in the liked table when users unlike the post
 * login()
  - Allowing users to login and checking if user provided the correct username and password
 * logout()
  - logging users out of the site and clearing the session
 * register()
  - registering new users and making sure they provide a username which isn't already taken and a password then inserting the new user's data into the users table in the project's database

 In project.db file you will find the database for this prject containing four tables which are
  * users table including
   - id
   - username
   - hash (for password hash)
   - date
   - bio
   - profilepic
   - backgroundpic
  * posts table including
   - id
   - user_id
   - postimg
   - posttxt
   - likes
   - date
   - user_username
  * comments table including
   - id
   - user_id
   - post_id
   - comment
   - date
   - user_username
  * liked table including
   - id
   - post_id
   - user_id