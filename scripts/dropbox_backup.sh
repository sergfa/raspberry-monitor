#!/usr/bin/env bash
BACKUP_SRC="/media/NASHDD1/share/private"
BACKUP_EXCLUDE="~/Downloads"
BACKUP_DST="/var/backups/$(date +"%Y")"
DROPBOX_DST="/Backup/$(date +"%Y")"
 
NOW=$(date +"%Y.%m.%d")
DESTFILE="$BACKUP_DST/$NOW.tgz"
 
echo -e "Archiving folders"
sudo mkdir -p $BACKUP_DST
sudo tar -zcf "$DESTFILE" --exclude="$BACKUP_EXСLUDE" $BACKUP_SRC
 
echo -e "Uploading archive to DropBox"
/home/pi/raspberry-monitor/scripts/dropbox_uploader.sh upload "$DESTFILE" "$DROPBOX_DST/$NOW.tgz"
 
echo -e "Cleaning up..."
sudo rm -rf $BACKUP_DST

echo -e "Finished"
