# Proxmox 2N HA Monitor

Script monitors the other node in a 2-node proxmox cluster.  If the other node becomes unavailable it will start the virtual machines on itself assuming they are HA enabled.
This script only checks the status of the cluster quorum from the node it is running on.  

## Details
 * The VM start is triggered by setting the Expected Votes on the node to 1.  This triggers Proxmox to start the HA Virtual Machines.
 * This program does not not perform any fencing functions!
 * Warning: If a network issue is preventing quorum and this program is running on both nodes, you may encounter a situation where both nodes start the HA VMs.     

## Setup

 * Setup a 2 node Proxmox cluster (v5.4-3 - 6.1-3) w/ ZFS local storage.  (If shared storage is available, that would be preferrable)
 * Enable Virtual Machine replication to the other node every 5 minutes or so (If using shared storage, replication is not needed)
 * Add the Virtual Machine as a High Availability resource in the cluster
 * Deploy the service file and enable for start on boot

## Deploying service

*  Make sure that the python3 path is correct
*  Set the correct path for the monitor_cluster.py script
*  Set the down_threshold
*  copy service file to /lib/systemd/system/
*  run `systemctl daemon-reload` to relaod the daemon
*  run `systemctl enable monitor_cluser.service` to start the service at boot
*  run `systemctl start monitor_cluster.service` to start the service now