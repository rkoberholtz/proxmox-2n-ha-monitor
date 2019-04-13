import subprocess
import sys
import getopt
import time
import logging
import os

def main(argv):

    logfile = "/var/log/monitor_2n_cluster.log"
    down_threshold = 5

    try:
        opts, args = getopt.getopt(argv,"htl",["down_threshold="])
    except:
        optUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            optUsage()
            sys.exit()
        elif opt in ("-t", "--down_threshold"):
            down_threshold = arg
        elif opt in ("-l", "--logfile"):
            logfile = arg

    logging.basicConfig(filename=logfile,level=logging.DEBUG)

    logging.debug("Process Started...logfile: %s]" % logfile)
    
    log_exists = os.path.exists(logfile)

    if not log_exists:
        os.mknod(logfile)

    while True:
        
        logging.debug("--%s-- Starting Check Process" % time.strftime("%Y%m%d-%H%M%S"))

        conn_failures = 0
        down_threshold = int(down_threshold)
        for i in range(down_threshold):
        
            time.sleep(60)
            
            j = i + 1
            cmd = "ha-manager status"
            #cmd = "ssh -q -o BatchMode=yes -o ConnectTimeout=10 %s echo 2>&1 && echo $host SSH_OK || echo $host SSH_NOK" % monitored_node_ip
            process = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE)
            status, err = process.communicate()
       
            #print(status)

            if "dead?" in str(status):
                cmd = "pvecm status | grep 'Expected votes'"
                process - subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE)
                vote_status, vote_err = process.communicate()
                if "Expected votes:   2" in str(vote_status):
                    setExpected()
                logging.debug("Check %s of %s: Quorum NOT OK, 1 node offline - expected quorum has been set to 1" % (j, down_threshold))
            elif "quorum OK" in str(status):
                logging.debug("Check %s of %s: Quorum OK" % (j, down_threshold))
            elif "No quorum on node" in str(status):
                logging.debug("Check %s of %s: Quorum NOT OK" % (j, down_threshold))
                conn_failures += 1
            else:
                logging.debug("An Unknown Check Result has been recievedi: %s" % status)
            
        
        if conn_failures < down_threshold:
            logging.debug("Cluster OK")
        elif conn_failures >= down_threshold: 
            logging.debug("No Quorum for %s!  Starting VMs on this NODE!" % down_threshold)
            setExpected()
                  
        logging.debug("Number of connection failures: %s - Sleeping for 15 seconds" % conn_failures)

def setExpected():

    logging.debug("Setting quorum expected nodes to 1")
    cmd = "pvecm expect 1"
    process = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE)
    out, err = process.communicate()
    logging.debug("result of '%s': %s | %s" % (cmd, out, err))
    return 0

def optUsage():

    print("General Help:")
    print("  This program monitors the availability of the specified ProxMox Node IP address.  If the node become unreachable it is assumed to be offline and runs the required commands to start the Virtual machines configured for HA on this node.")
    print("")
    print("  --down_threshold= | Threshold (in minutes) that the node needs to be down before considered down. Default is 5 min")
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
