#!/bin/bash

set -e

PROJECT_DIRECTORY=$1
USER_=$2
UID_=$3

useradd -l -u $UID_ -G sudo -md /home/$USER_ -s /bin/bash -p $USER_ $USER_
sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
mv /venv /venv_hack
mkdir /venv
chown $USER_:$USER_ /venv

## IMPORTANT to put single quotes around EOL here so that the stuff does not get interpretted
cat >/home/$USER_/.bashrc <<'EOL' 
export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h--codepod:\w\$ "
EOL

chown $USER_:$USER_ /home/$USER_/.bashrc

## IMPORTANT to put single quotes around EOL here so that the stuff does not get interpretted
cat >/the_script.sh <<'EOL' 
#!/bin/bash
set -e

export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h--codepod:\w\$ "
export HOME=/home/$USER_

# symbolic links to files in /home/user to the home directory
if [ -d /home/user ]; then
    echo "test"
    ls /home
    ls /home/user/.*
    for filename in $(ls -A /home/user/); do
        ln -s /home/user/$filename ~/$filename
    done
fi

cd $PROJECT_DIRECTORY
cp -r /venv_hack/* /venv/

source /venv/bin/activate
if [ -f "/theiapod_init" ]; then
	echo "RUNNING python /theiapod_init"
	python /theiapod_init
fi

if [ -f "/codepod_init" ]; then
	echo "RUNNING python /codepod_init"
	python /codepod_init
fi
/bin/bash
EOL

chmod a+x /the_script.sh

cd /home/$USER_
sudo -u $USER_ bash -c "PROJECT_DIRECTORY=$PROJECT_DIRECTORY USER_=$USER_ /the_script.sh"
