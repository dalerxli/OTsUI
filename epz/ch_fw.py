#import epz library
import epz.epz3 as epz
#instantiate the forwarder and start 
fw = epz.Forwarder()
fw.daemon = True
#note: fw.daemon is internally set to False, to avoid closure of the 
#forwarding thread just at the end of the script.
fw.start()