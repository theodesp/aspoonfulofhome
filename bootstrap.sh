#!bin/bash

###############################################################################
# Install prerequisites
###############################################################################

# aptitude configuration
APTITUDE_OPTIONS="-y"
export DEBIAN_FRONTEND=noninteractive

# run an aptitude update to make sure python-software-properties
# dependencies are found
apt-get update

# add the reddit ppa for some custom packages
apt-get install $APTITUDE_OPTIONS python-software-properties

cat <<PACKAGES | xargs apt-get install $APTITUDE_OPTIONS
postgresql-server-dev-9.3
postgresql-9.3
redis-server
PACKAGES

# Add repository
git clone https://thdespou@bitbucket.org/thdespou/theoliveoilbakers.git

# Create ssh keys
ssh-keygen -t rsa -b 4096 -C "thdespou@hotmail.com"

# Node.js
add-apt-repository ppa:chris-lea/node.js
apt-get update
apt-get install nodejs

npm install -g bower coffee-script

bower install

