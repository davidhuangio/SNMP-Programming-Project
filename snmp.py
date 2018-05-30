from easysnmp import Session, snmp_get
import time

#David Huang 008841430

def getBandwidth(snmpSession, timeInterval, numSamples):
	
	for i in range (0,int(numSamples)):
		firstRead = []
		secondRead = []

		for interface in snmpSession.walk(".1.3.6.1.2.1.2.2.1.10"):
			firstRead.append(int(interface.value)) #Grab ifInOctets from interface

		time.sleep(float(timeInterval)) #Wait time interval between samples
		
		for interface in snmpSession.walk(".1.3.6.1.2.1.2.2.1.10"): #Grab ifInOctets again
			secondRead.append(int(interface.value))
		
		print "Interval " + str(i + 1) + " for " + str(timeInterval) + " seconds: "

		for i in range(0, len(snmpSession.walk(".1.3.6.1.2.1.2.2.1.10")) ):	
			inputBandwidth = ( (secondRead[i] - firstRead[i]) * 8 ) / (float(timeInterval) * int(numSamples) * 1048576) #Octets->Bits->MBps
			print "Interface: " + snmpSession.walk(".1.3.6.1.2.1.2.2.1.2")[i].value + " Down: " + str(inputBandwidth) + "Mbps "
					

print "Please enter in the following:"
print "IP Address of Agent (or 'localhost' for local use): " 
agentAddress = raw_input()
print "Please enter in the community we will be using: "
communitySet = raw_input()
print "Please enter in the number of bandwidth samples: "
sampleCount = raw_input()
print "Please enter in the time interval in seconds between each sample: "
intervalCount = raw_input()

# Create an SNMP session to be used for all our requests
session = Session(hostname=agentAddress , community=communitySet , version=2)

#Retrieve contact and location as introduction
print "Hello " + session.get(('sysContact', '0')).value + " from: " + session.get('sysLocation.0').value

interfaces = session.walk(".1.3.6.1.2.1.2.2.1.2") #ifTable.ifDescr Interface Table Names
print ""
print "Interfaces"
print "--------------"
count = 1
for item in interfaces:
    print str(count) + " " + item.value
    count = count + 1

neighbors = session.walk(".1.3.6.1.2.1.4.22.1.2") #ARP Table IP Neighbors ipNetToMediaPhysAddress (no loopback or host IP included)
print ""
print "Neighbors"
print "---------------"
count = 1
for item in neighbors:
    print str(count) + " " + item.oid_index[2:]
    count = count + 1
print ""
print "Network Bandwidth"
print "-----------------"
getBandwidth(session,intervalCount,sampleCount)
