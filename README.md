# Proxmox 2N HA Monitor

Script monitors the other node in a 2-node proxmox cluster.  If the other node becomes unavailable it will start the virtual machines on itself assuming they are HA enabled.