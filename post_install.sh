#!/bin/sh

cp index-images gallery.py convert.py /usr/local/bin/
chmod +x /usr/local/bin/index-images

rm /usr/local/www/nginx
mkdir -p /usr/local/www/nginx
mkdir -p /mnt/images

wget "https://picsum.photos/2000/3000" -O/mnt/images/20170913_174448.jpg

sysrc -f /etc/rc.conf nginx_enable="YES"
echo "@reboot root /usr/local/bin/index-images >/dev/null" | crontab -

service nginx start

index-images
