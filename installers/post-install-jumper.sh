apt-get install -y python3-dev python3-pip

git clone https://github.com/needmorecowbell/jumper && cd jumper/master
screen -S jumperMaster -dm python3 master.py
