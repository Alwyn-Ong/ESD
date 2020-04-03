# ESD

account.py -> port: 8000
profile.py -> port: 2000
recommendation.py -> port: 9000
match.py -> port:
image.py -> port:

# open wamp
# create databases, sglovelah_chat, sglovelah_profile, sglovelah_account, sglovelah_match, sglovelah_recommendation, sglovelah_image
# cd into /backend/dbscripts and import all files to populate each database accordingly
# `` pip3 install flask-socketio
# cd into /backend/chatms, run all chatsocketone/two/three/four/five.py, run chat.py
# cd into /backend, run image.py match.py profile.py recommendation.py account.py

To run the docker image, 
1. docker pull alwynong/account:1.0.0
2. docker run -p 8000:8000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/sglovelah_account alwynong/account:1.0.0