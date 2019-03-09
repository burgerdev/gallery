# FreeNAS Gallery

This is some custom code to deploy an image server as a FreeNAS plugin. 

**This will probably not work on your machine!**
**This will execute untrusted and unverified input with `os.system`!**

## Usage

Install the iocage with

```sh
wget https://raw.githubusercontent.com/burgerdev/gallery/master/gallery.json
iocage fetch -P --name gallery.json dhcp="on" vnet="on" bpf="yes" boot="on"
```

Mount images from an Android phone to `/mnt/images`, restart the jail
and watch your gallery grow at http://gallery/.

