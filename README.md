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
# Configuration & Usage

> Below and the rest of the documnetation will explain usage when NodeDefender is installed using pypi
> For installation from source $ nodedefender is changed to $ ./manage.py

```
$ nodedefender run
```
Will start the application and give you the possibility to deploy configuration and initial superuser.
Once complete; restart the application and the new configuration will be used.
