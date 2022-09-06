import socket
import sys
import os
import datetime
 
# Clear the screen
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
 
cls()
 
# Defining a target host, start and end ports
if len(sys.argv) == 4: 
    # We have command line options so lets use those
 
    # translate hostname to IPv4 
    remoteServerIP = str(socket.gethostbyname(sys.argv[1]))
 
    if len(remoteServerIP) == 0:
        print("A hostname or IP address is required!")
        sys.exit()
 
    startPort = int((sys.argv[2]))
    endPort = int((sys.argv[3]))
else: 
    # We don't have the correct number of command line options so prompt for input
    print("Command Line Usage: PortScanner.py <host> <start port> <end port>\n")
 
    remoteServer = input("Enter a remote hostname or IP to scan: ")
    remoteServerIP = socket.gethostbyname(remoteServer)
 
    if len(remoteServerIP) == 0:
        print("A hostname or IP address is required!")
        sys.exit()
 
    startPort = input("Start at port (0): ")
    endPort = input("End at port (1023): ")
 
    # If the user did not provide ports use the defaults
    if not startPort:
        startPort = 0
 
    if not endPort:
        endPort = 1023
 
# Print a banner with information on which host we are about to scan
openPortCount = 0
startTime = datetime.datetime.now()
 
print("=" * 60)
print("Please wait, scanning remote host", remoteServerIP)
print("Scanning started at: " + startTime.strftime("%x %X"))
print("Please CTRL+C to cancel")
print("=" * 60)
print("Open Ports:")
 
# Scan the ports using the range function to loop 
try:
    for port in range(int(startPort),int(endPort)):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print(" Port {}:     Open".format(port))
            openPortCount += 1
        sock.close()
 
except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()
 
except socket.gaierror:
    print("Error - Could not resolve hostname.")
    sys.exit()
 
except socket.error:
    print("Error - Couldn't connect to server")
    sys.exit()
 
endTime = datetime.datetime.now()
runTime = endTime - startTime
runTime_in_s =  runTime.total_seconds()
 
runtimeDays    = divmod(runTime_in_s, 86400)        # Get days (without [0]!)
runtimeHours   = divmod(runtimeDays[1], 3600)               # Use remainder of days to calc hours
runtimeMinutes = divmod(runtimeHours[1], 60)                # Use remainder of hours to calc minutes
runtimeSeconds = divmod(runtimeMinutes[1], 1)               # Use remainder of minutes to calc seconds
 
# Print end information to screen
print("-" * 60)
print("Scanning complete")
print(" Duration: %d days, %d hours, %d minutes and %d seconds" % (runtimeDays[0], runtimeHours[0], runtimeMinutes[0], runtimeSeconds[0]))
print(" Ports scanned " + str(startPort) + " to " + str(endPort))
print(" " + str(openPortCount) + " open port(s) found")
print("-" * 60)
 
# Wait for the users input to terminate the program
input("Press the enter key to exit")
