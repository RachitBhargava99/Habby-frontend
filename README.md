# Eventster
Welcome to Eventster - time to see only the events you love, only the ones around you!

This is the supporting client for the main application and must not be confused with the server module.

This application requires you to start the <code>run.py</code> file to start the application.

## URL's to Access Pages
### <pre>/                              GET</pre>
Homepage - You may provide the categories and ZIP Code to see the results.
<hr>

### <pre>/                              POST</pre>
Results Page - You may see the results based on the most recent query you provided.
<hr>

### <pre>/?page=<Int>                   GET</pre>
Results Page - You may see the results based on the most recent query you provided
and access the exact page as mentioned in the URL parameter.
<hr>

### <pre>/event/<Int:local_event_id>    POST</pre>
Event Page - You may see details about the event through this page
and also browse to Eventbrite's website to make any reservations, if needed.
<hr>

## Google App Engine Requirements
This client was initially built to be deployed using Google App Engine.
However, you may deploy it freely in any other environment.
As of now, the application has been tested on Windows machine as well.
<hr>

## Contact Info
In case of any queries, please feel free to contact Rachit Bhargava (developer) at rachitbhargava99@gmail.com.

## Third-Party Use
This application cannot be used for any unauthorized uses.
If you are interested in using the application for any purposes, please contact the developer for permissions.