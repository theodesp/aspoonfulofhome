#!bin/bash

PROJECT = "theoliveoilbakers"

###############################################################################
# Install prerequisites
###############################################################################

set -e

echo "Starting initial provision"

# locale configuration
locale="en_US.UTF-8"
timezone="Europe/Nicosia"
/usr/sbin/locale-gen $locale
/usr/sbin/update-locale LANG=$locale LC_ALL=$locale LANGUAGE=$locale
echo $timezone > /etc/timezone

# aptitude configuration
APTITUDE_OPTIONS="-y"
export DEBIAN_FRONTEND=noninteractive

# run an aptitude update to make sure python-software-properties
# dependencies are found
apt-get update

# add some custom packages
apt-get install $APTITUDE_OPTIONS python-software-properties

cat <<PACKAGES | xargs apt-get install $APTITUDE_OPTIONS
postgresql-server-dev-9.3
postgresql-9.3
redis-server
git-core
python-setuptools
libpq-dev
python-dev
libjpeg-dev
PACKAGES
# Add repository
git clone https://thdespou@bitbucket.org/thdespou/theoliveoilbakers.git theoliveoilbakers

# install python packages
pip install -r theoliveoilbakers/requirements.txt

# Node.js
add-apt-repository ppa:chris-lea/node.js
apt-get update
apt-get install nodejs

npm install -g bower coffee-script

###############################################################################
# Postgres
###############################################################################

PG_VERSION = 9.3

# Create the db user
user_exists=`sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$PROJECT'"

if [[ $user_exists != "1" ]]
then
    su postgres -c "createuser -s '$PROJECT'"
    sudo -u postgres psql -c "CREATE ROLE '$PROJECT' LOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;"
fi
# Restart the service so the changes take effect
sudo service postgresql restart

# Create database
db_exists=`sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$PROJECT'"`
sudo -u postgres psql -c "ALTER USER '$PROJECT' WITH PASSWORD '$PROJECT';"
if [[ $db_exists != "1" ]]
then
su postgres -c "createdb -O '$PROJECT' '$PROJECT'"
fi



venvfolder = "$PROJECT-env"

virtualenv --no-site-packages $venvfolder
source $venvfolder/bin/activate

cd $PROJECT
bower install
virtualenv
python manage.py migrate

