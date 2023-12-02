import os
import sys
import io

def IsPi():
    osval = os.name
    if osval == 'posix':
        try:
            with io.open('/proc/cpuinfo','r') as cpuinfo:
                for line in cpuinfo:
                    if line.startswith('Hardware'):
                        if "BCM" in line:
                            return True
        except Exception:
            return False

    return False