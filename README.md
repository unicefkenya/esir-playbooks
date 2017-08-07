# Playbooks
A collection of [Ansible][1] scripts and templates used to deploy e-SIR platform tools.


## Setup
To run the stuff herein, you need Ansible. To use [Ansible][1] you might need [pycrypto][2].
To build pycrypto, you need the latest python (2.1 <= ver <= 3.3) development libs & headers.
Stick with python v2.7 for now. It's the current status quo.
In a nutshell, if you're using debian/ubuntu :- `apt-get install python-dev`

***Clone this repo***

    $ git clone git@github.com:onaio/esir-playbooks.git playbooks && cd playbooks

***Install Requirements***

    $ sudo apt-get install python-pip python-dev libssl-dev
    $ sudo pip install python-virtualenvwrapper
    $ export WORKON_HOME=$HOME/.virtualenvs
    $ mkdir $WORKON_HOME
    $ source /usr/local/bin/virtualenvwrapper.sh
    $ mkvirtualenv playbooks
    $ pip install -r requirements/base.pip`

***Install required roles***

    $ ansible-galaxy install -r requirements/roles.yml -p roles

##  Deployment Commands

***Deploying Data Platform API***

    $ ansible-playbook -i inventory/esir-api.ini esir-api.yaml --vault-password-file [path to password file]

***Deploying Data Platform UI***

    $ ansible-playbook -i inventory/esir-data.ini esir-data.yaml --vault-password-file [path to password file]

***Deploying e-SIR dashboard***

    $ ansible-playbook -i inventory/esir.ini esir.yaml --vault-password-file [path to password file]

***Deploying Enketo***

    $ ansible-playbook -i inventory/enketo.ini enketo.yaml --vault-password-file [path to password file]


[1]: http://www.ansible.com
[2]: https://pypi.python.org/pypi/pycrypto
