import sys
from datetime import datetime

def getsec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
#end getsec


def checkforlinewitheu(lineoffile):
	try:
		linewitheu=regel.index("<cont:2>EU") #regel met eu
		return 1
	except:
		return 0 #regekl zonder eu headers enzo
#end checkfor eu


def checkforlinewithouttime(lineoffile):
	try:
		linewithouttime=regel.index("<call:") #regel met tijd
		return 0
	except:
		return 1 #regekl zonder tijd headers enzo
#end checkfor linewithouttime


def checkfortimeoff(lineoffile):
	try:
		strt=regel.index("<time_off:6>")
		timeoff=regel[strt+12:strt+19]
		timeoff1=timeoff
		timeoff=timeoff1[0:2] + ':' + timeoff1[2:4] + ':' + timeoff1[4:]
	except:
		timeoff='0'
	return timeoff 
#end checkfortimeon


def checkfortimeon(lineoffile):
	try:
		strt=regel.index("<time_on:6>")
		timeon=regel[strt+11:strt+18]
		timeon1=timeon
		timeon=timeon1[0:2] + ':' + timeon1[2:4] + ':' + timeon1[4:]
	except:
		timeon='0'
	return timeon
#end checkfortimeon



#start main
 
if len(sys.argv) != 2:
	print('Voer een ADIF in... Syntax -> Python3 doadif.py xxx.adif')
	sys.exit("Probeer nog eens") 
else:
	maandadiffile = sys.argv[1]

adifforupload = open("yl3jdSL.adi", "w")
adiffile = open(maandadiffile, "r")

regel=1
while regel:
	regel=adiffile.readline()
	if checkforlinewithouttime(regel) == 1 :
		adifforupload.write(regel)
		print(regel)
	else :	
		if checkforlinewitheu(regel) == 1 :
			timeoff=checkfortimeoff(regel)
			timeon=checkfortimeon(regel)
			#print(timeoff,"  ",timeon)
			if timeon != '0':	# we hebben en aan  tijd in het adif
				try: # voor het geval dat de offtime kleiner is dan on time dus een negatieve tijd.
					duration=getsec(str(datetime.strptime(timeoff[0:8], "%H:%M:%S") - datetime.strptime(timeon[0:8], "%H:%M:%S")))
					if duration > 299 :
						print(duration)
						print(regel)
						print("----------------------------------------")
						adifforupload.write(regel)
				except:
					print("----------------------------------------")
					print("QSO offtime is kleiner dan QSO ontime check tijd !!!!!!!")
					print(regel)
					print("----------------------------------------")

adiffile.close()
adifforupload.close()