# OSCMT - an Open Source Case Management Tool
This repository contains the project for my Bachelor's Thesis at [HS
Esslingen](https://hs-esslingen.de) under Prof. Dr.-Ing. [Harald
Melcher](https://hs-esslingen.de/~melcher) and [SySS GmbH](https://syss.de)
under Dr. Klaus Tichmann.

## Background
The goal of my thesis was to create a case management software for digital
forensics cases. After we looked at current software solutions we decided to
create a software solution with the Django framework in Python 3.4. This
repository is the result.

## Installation
### Dependencies
If you want to use the ansible-playbook I provided, you need:

* ansible >= 2.2.1
* a Debian-based OS on the host where you want to install the software (preferably Debian Jessie or later)
* a ssh-login on said host that has sudo-permissions
* Python2.7 on said host

If this is provided, ansible will do the rest for you.

If you want to install the software by hand, you will need:

* Python3.4
* a WSGI-server, e. g. uWSGI
* a web-server, e. g. NGINX

### Deployment

If you don't use the ansible-playbook I expect that you know what you're doing.
Please connect OSCMT to your wsgi-server and let it be served by a webserver.

Using the ansible-playbook:

### Preparation
```bash
# Make sure your ansible-hosts-file contains the appropriate IP address or fqdn:

# become root
sudo -s

# set appropriate value for FQDN (an IP address works too)
FQDN="YOUR_IP_OR_FQDN_HERE"
# append relevant information
cat << EOF >> /etc/ansible/hosts
[oscmt]
${FQDN} ansible_ssh_private_key_file='/path/to/your/ssh/keyfile'
EOF

# exit root
exit

# set appropriate values for FQDN, REMOTEUSER, KEYFILE and CERTFILE
FQDN="your fqdn here"
REMOTEUSER="your remote user here"
KEYFILE="name.of.your.keyfile.key"
CERTFILE="name.of.your.certfile.crt"

# set the correct remote user in provision.yml
sed -E -i "s/^(\s+)remoteuser:.*/\1remoteuser: ${REMOTEUSER}/m" ansible-playbooks/provision.yml

# set the correct fqdn in provision.yml
sed -E -i "s/^(\s+)fqdn:.*/\1fqdn: ${FQDN}/m" ansible-playbooks/provision.yml

# set the correct keyfile
sed -E -i "s/^(\s+)keyfile:.*/\1keyfile: ${KEYFILE}/m" ansible-playbooks/provision.yml

# set the correct certfile
sed -E -i "s/^(\s+)certfile:.*/\1certfile: ${CERTFILE}/m" ansible-playbooks/provision.yml
```

Afterwards, look over the provision.yml file to make sure everything worked correctly.
```bash
view ansible-playbooks/provision.yml
```

If everything appears to be correct, proceed to deploy OSCMT.

### Execution
```bash
SECRET_KEY=$(python -c 'import random; import string; print("".join([random.SystemRandom().choice("{}{}".format(string.ascii_letters, string.digits)) for i in range(50)]))')

DB_PASSWORD=$(python -c 'import random; import string; print("".join([random.SystemRandom().choice("{}{}".format(string.ascii_letters, string.digits)) for i in range(50)]))')

# If you want to set those variables on your own please make sure they don't contain single or double quotes, otherwise the next line *WILL* fail and you *WILL* be sad.
# If shell expansion doesn't work properly your config files will contain errors and you will spend the better part of two work days to figure out where that 400 Bad Request from
# nginx suddenly came from. (It came from uwsgi which in turn threw errors due to django misbehaving which misbehaved due to wrong config files.) You have been warned.

ansible-playbook provision.yml --ask-become-pass --extra-vars "secret_key=${SECRET_KEY} dbpassword=${DB_PASSWORD} fqdn=${FQDN}"
```

This will ask you for the sudo-password of your user on the host. After that, it
will use the ansible-playbook to install OSCMT, ensuring that the SECRET_KEY in
Django's settings.py and the database password will be something truly random.

If you want to be able to access the database directly, it is probably a good
idea to save the password.

```bash
echo $DB_PASSWORD > db-pwd.txt
```

Backup that file to a safe place where it can't be accessed by unauthorised users.

Since we don't want to share secret keys and db passwords with anybody else, we now get rid of the environment variables.

```bash
unset DB_PASSWORD
unset SECRET_KEY
```

## Configuration

After the playbook has run, you need to connect to the remote host and create a superuser for django.

```bash
ssh ${REMOTEUSER}@${FQDN}

sudo -s

source /var/www/env/oscmt_env/bin/activate

python /var/www/oscmt/oscmt/manage.py createsuperuser
```

Tell the manage.py script everything it needs to know, afterwards you should be
able to navigate to ${FQDN} and log in.

After logging in as the superuser (henceforth "admin"), you can use OSCMT as a
single user. Since this is normally a bad idea, you probably want to create
groups and users next.

More detail can be found in [the manual](manual/manual.md)

## Call for Participation
If you have an improvement for the software please throw me a pull request.
