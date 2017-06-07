# Playbooks
A collection of [Ansible][1] scripts and templates used to deploy various Kobotoolbox
projects to various environments.


## Setup
To run the stuff herein, you need Ansible. To use [Ansible][1] you might need [pycrypto][5].
To build pycrypto, you need the latest python (2.1 <= ver <= 3.3) development libs & headers.
Stick with python v2.7 for now. It's the current status quo.
In a nutshell, if you're using debian/ubuntu :- `apt-get install python-dev`

For local "dev" deployments, you will need to install [Virtualbox][3] and [Vagrant][2].
Download Virtualbox [from here][4] and Vagrant [from here][6]
or feel free to install those from your distro's repos (and brew if using OSX).


***Clone this repo***
`git clone git@github.com:onaio/kira-playbooks.git playbooks && cd playbooks`

***Install Requirements***
`sudo pip install python-virtualenvwrapper`
`export WORKON_HOME=$HOME/.virtualenvs`
`mkdir $WORKON_HOME`
`source /usr/local/bin/virtualenvwrapper.sh`
`mkvirtualenv playbooks`
`pip install -r requirements/base.txt`

***Install required roles***
`ansible-galaxy install -r requirements/roles.yml -p roles`

##  Deployment Commands

***Deploying dkobo***

`ansible-playbook -i inventory/dkobo.ini dkobo.yaml --extra-vars="" --vault-password-file [path to password file]`

***Deploying kobocat***

`ansible-playbook -i inventory/kobocat.ini kobocat.yaml  --extra-vars="" --vault-password-file [path to password file]`

***Deploying enketo***

`ansible-playbook -i inventory/enketo-kobocat.ini enketo-kobocat.yaml  --extra-vars="" --vault-password-file [path to password file]`


## Usage (dev environment)
For development deploys, first rename `ansible.cfg.vagrant` to `ansible.cfg`.
This [config][8] tells ansible to use the vagrant [remote user][9] & [public key][7]

`vagrant up` - (downloads and) brings up the local Virtualbox dev VM we'll deploy to.
`ansible-playbook -i inventory/vagrant_vm_single.ini onadata.yaml -vvvv` -
deploy onadata to the dev vm that vagrant just spun up

[1]: http://www.ansible.com
[2]: https://www.vagrantup.com
[3]: https://www.virtualbox.org
[4]: https://www.virtualbox.org/wiki/Downloads
[5]: https://pypi.python.org/pypi/pycrypto
[6]: https://www.vagrantup.com/downloads.html
[7]: https://github.com/mitchellh/vagrant/tree/master/keys
[8]: http://docs.ansible.com/intro_configuration.html
[9]: http://docs.ansible.com/playbooks_intro.html#hosts-and-users
