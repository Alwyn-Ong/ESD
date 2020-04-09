@echo off
start docker pull alwynong/account:1.0.0 & docker run -p 8000:8000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/sglovelah_account alwynong/account:1.0.0
