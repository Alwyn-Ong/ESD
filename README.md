# ESD

# make sure wamp is on.
# create databases, sglovelah_chat, sglovelah_profile, sglovelah_account, sglovelah_match, sglovelah_recommendation, sglovelah_image
# cd into /backend/dbscripts and import all files to populate each database accordingly
# `` pip3 install flask-socketio
# cd into /backend/chatms, run all chatsocketone/two/three/four/five.py, run chat.py
# cd into /backend, run image.py match.py profile.py recommendation.py account.py

To run the entire app,
1. cd into project directory, click on "start_microservices" batch file 
2. make sure docker is running, click on "start_docker" batch file (to start account docker)
3. right click on index.html, click on open in default browser.
4. you should be able to stimulate the scenario and log in

** if you're unable to log in. 
1. open another cmd and docker pull alwynong/account:1.0.0
2. docker run -p 8000:8000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/sglovelah_account alwynong/account:1.0.0