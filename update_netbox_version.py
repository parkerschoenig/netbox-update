#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

# Get current Netbox version
netbox_version=$(grep -Po "(?<=VERSION = ')[^']+" /opt/netbox/netbox/netbox/settings.py)

# Format current Netbox version
netbox_version="v${netbox_version//./.}"
netbox_version=$(echo $netbox_version | sed 's/ \.$//')

# Get latest Netbox version from Github
github_version=$(curl -s 'https://api.github.com/repos/netbox-community/netbox/releases/latest' | grep -oP '"tag_name": "\K(.*)(?=")')

# Compare versions
if [ "$netbox_version" != "$github_version" ]; then
  # Update Netbox
  echo "New Netbox version found, updating"
  sleep 2
  cd /opt/netbox
  sleep 2
  git checkout master
  sleep 30
  git pull origin master
  sleep 30
  ./upgrade.sh
  sleep 120
  systemctl restart netbox netbox-rq

  # Print old and new versions
  echo "Netbox successfully updated from version $netbox_version to $github_version"

  # Send email
  echo -e "Subject: Netbox Version Status\n\n####################################### THIS IS AN AUTOMATED EMAIL #######################################\n\nNetbox is scheduled to check for updates the 1st and 15th of each month and will
automatically update if a new version is found.\n\nSTATUS: Netbox successfully updated from $netbox_version to $github_version \n\n#########################################################################################################" | sendmail -t -cc <email-1> <email-2>

else
  # Netbox is up to date
  echo "Netbox is up to date, no update needed currently on $netbox_version"

   # Send email
  echo -e "Subject: Netbox Version Status\n\n####################################### THIS IS AN AUTOMATED EMAIL #######################################\n\nNetbox is scheduled to check for updates the 1st and 15th of each month and will
automatically update if a new version is found.\n\nSTATUS: Netbox is up to date, no update needed ($netbox_version) \n\n#########################################################################################################" | sendmail -t -cc <email-1> <email-2>
fi
