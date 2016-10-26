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

## Content
This repository contains the clean version of the software, ready for your use.

## Installation
### Dependencies
If you want to use the ansible-playbook I provided, you need:

* ansible >= 2.0.0
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

```bash
export SECRET_KEY=$(python -c 'import random; import string; print("".join([random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(50)]))')

export DB_PASSWORD=$(python -c 'import random; import string; print("".join([random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(50)]))')

export FQDN="whatever your fqdn looks like"

ansible-playbook provision.yml --ask-become-pass --extra-vars 'secret_key="${SECRET_KEY}" dbpassword="${DB_PASSWORD}" fqdn="${FQDN}"'
```

This will ask you for the sudo-password of your user on the host. After that, it
will use the ansible-playbook to install OSCMT, ensuring that the SECRET_KEY in
Django's settings.py and the database password will be something truly random.

If you want to be able to access the database directly, it is probably a good
idea to save the password.

```bash
echo $DB_PASSWORD > db-pwd.txt
```

After the playbook has run, you need to connect to the remote host and create a superuser for django.

```bash
ssh remoteuser@fqdn

sudo -s

source /var/www/env/oscmt_env/bin/activate

python /var/www/oscmt/oscmt/manage.py createsuperuser
```

Tell the manage.py script everything it needs to know, afterwards you should be
able to navigate to fqdn.tld and log in.

After logging in as the superuser (henceforth "admin"), you can use OSCMT as a
single user. Since this is normally a bad idea, you probably want to create
groups and users next.

Navigate to the /admin/ page next, here you can create groups and users to your
liking, as well as managing permissions for said groups and users.

When you're done with the admin account, log out and log back in as a regular
user and start documenting your cases.

## Call for Participation
If you have an improvement for the software please throw me a pull request.
