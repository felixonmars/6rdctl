6rdctl
======

6rd Control Tool

# Installation
## Arch Linux (AUR):
    $ yaourt -S 6rdctl-git

# Usage
    $ 6rdctl -h
    usage: 6rdctl [-h] [-d] [-i [INTERFACE]] [-p [PREFIX]] [-r [ROUTER]]
                  [--ip [IP]] [--radvd] [--radvd-interface [RADVD_INTERFACE]]
    
    6rd Control Tool
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --delete          Remove the corresponding 6rd interface
      -i [INTERFACE], --interface [INTERFACE]
                            WAN interface to use, default: eth0
      -p [PREFIX], --prefix [PREFIX]
                            6rd prefix to use, default: 2001:e41
      -r [ROUTER], --router [ROUTER]
                            6rd router to use, default: 61.211.224.125
      --ip [IP]             Specify custom IP to use for calculating 6rd address,
                            default: gather from WAN interface
      --radvd               Change /etc/radvd.conf accordingly
      --radvd-interface [RADVD_INTERFACE]
                            LAN interface to use, default: eth1
