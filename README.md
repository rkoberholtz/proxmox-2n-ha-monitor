# Proxmox 2N HA Monitor

Script monitors the other node in a 2-node proxmox cluster.  If the other node becomes unavailable it will start the virtual machines on itself assuming they are HA enabled.
This script only checks the status of the cluster quorum from the node it is running on.  It does not not perform any fencing fucntions.  If a network issue is preventing quorum, you will have a situation where both node have the VMs started.

## Deploying service

*  Make sure that the python3 path is correct
*  Set the correct path for the monitor_cluster.py script
*  Set the down_threshold
*  copy service file to /lib/systemd/system/
*  run `systemctl daemon-reload` to relaod the daemon
*  run `systemctl enable monitor_cluser.service` to start the service at boot
*  run `systemctl start monitor_cluster.service` to start the service now