[<img src="logo.png">](https://www.nodedefender.com/)
[NodeDefender](https://www.nodedefender.com) is an Open- Source program for controlling multiple Z-Wave devices connected to multiple gateways.
This programs is exclusivly designed to work with [CTS-iCPE](http://cts-icpe.com). 

# Requirements

- Linux System
- Python3
- Python3-dev
- Python-virtualenv
- libpq-dev

# Installation

### Installation from pypi with "pip":
```
 $ pip install nodedefender
```
### Installation from source(git)
```
$ git clone https://github.com/CTSNE/NodeDefender.git
$ cd NodeDefender
$ virtualenv -p python3 py
$ source py/bin/activate
(venv)$ pip install -r requirements.txt
```
## Deployment & Configuration

> If installation is done from Source you should use the manage.py
> Explanation describes the usage where nodedefender is installed from pypi.
> The two operate in the same manner though.

Start the server by running
```
$ nodedefender run
```
You should not be able to setup the host at "HOSTNAME:5000".
Once configuration and initial superuser has been configured reboot the server.
