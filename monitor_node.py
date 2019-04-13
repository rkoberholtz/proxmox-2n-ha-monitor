import subprocess
import sys
import getopt
import time
import logging

def main(argv):

    monitored_node_ip = ''
    logfile = "/var/log/monitored_node.log"
    down_threshold = 5
    status = ''

    try:
        opts, args = getopt.getopt(argv,"hn:tl",["node_ip="])
    except:
        optUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            optUsage()
            sys.exit()
        elif opt in ("-n", "--node_ip"):
            monitored_node_ip = arg
        elif opt in ("-t", "--down_threshold"):
            down_threshold = arg
        elif opt in ("-l", "--logfile"):
            logfile = arg

    logging.basicConfig(filename=logfile,level=logging.DEBUG)

    logging.debug("Process Started...[monitored_node: %s | logfile: %s]" % (monitored_node_ip, logfile))

    while True:
        
        logging.debug("--%s-- Starting Check Process for %s" % (time.strftime("%Y%m%d-%H%M%S"), monitored_node_ip))

        conn_failures = 0
        for i in range(down_threshold):
        
            cmd = "ssh -q -o BatchMode=yes -o ConnectTimeout=10 %s echo 2>&1 && echo $host SSH_OK || echo $host SSH_NOK" % monitored_node_ip
            process = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE)
            status, err = process.communicate()
        
            if "SSH_OK" in str(status):
                logging.debug("Check %s of %s: OK" % (i, down_threshold))
            elif "SSH_NOK" in str(status):
                logging.debug("Check %s of %s: NOT OK" % (i, down_threshold))
                conn_failures += 1
            else:
                logging.debug("An Unknown Check Result has been recievedi: %s" % status)

        if conn_failures <= down_threshold:
            logging.debug("Node %s OK" % monitored_node_ip)
        elif conn_failures > down_threshold: 
            logging.debug("Node $s is UNAVAILABLE!  Starting VMs on this NODE!" % monitored_node_ip)
            startVMs()
                  
        logging.debug("Number of connection failures: %s - Sleeping for 15 seconds" % conn_failures)
        time.sleep(15)

def startVMs():

    logging.debug("Setting quorum 'expected' to 1")
    cmd = "pvecm expect 1"
    process = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE)
    out, err = process.communicate()
    logging.debug("result of '%s': %s | %s" % (cmd, out, err))
    return 0

def optUsage():

    print("General Help:")
    print("  This program monitors the availability of the specified ProxMox Node IP address.  If the node become unreachable it is assumed to be offline and runs the required commands to start the Virtual machines configured for HA on this node.")
    print("")
    print("  -n, --node_ip | IP Address of the ProxMox Node to be monitored")
    print("  -t, --node_up | Threshold (in minutes) that the node needs to be down before considered down. Default is 5 min")
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
