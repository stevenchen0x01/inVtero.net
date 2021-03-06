import clr
import sys
from sys import argv

import Analyze

clr.AddReferenceToFileAndPath("inVtero.net.dll")

from inVtero.net import *
from System.Diagnostics import Stopwatch
from System import Environment, String, ConsoleColor
from System.IO import File
from inVtero.net.Hashing import MetaDB

from Analyze import QuickSetup

#testFile = "C:\\Users\\files\\VMs\\Windows 10 x64-PRO-1703\\Windows 10 x64-PRO-1703-40599dd1.vmem"
#testFile = "d:\\Users\\files\\VMs\\Windows Server 2016\\Windows Server 2016-02431799.vmem"
#testFile = "C:\\Users\\files\\VMs\\Windows Server 2008 x64 Standard\\Windows Server 2008 x64 Standard-ef068a0c.vmem"

testFile = "C:\\Users\\files\\VMs\\Windows 10 x64-PRO-1703\\Windows 10 x64-PRO-1703-40599dd1.vmem"

print "Scanning input: " + testFile

TotalRunTime = Stopwatch.StartNew()
aBufferCount = 60000000

# local we have insane size capability
mdb = MetaDB("c:\\temp\\inVtero.net", 4096, 1024*1024*1024*16, aBufferCount)

#cloud is 4096 for now
#mdb = MetaDB("c:\\temp\\inVtero.net", 4096, 1024*1024*1024*16, aBufferCount)

mdb.cLoader.MaxBatchParallel = 200

vtero = QuickSetup(testFile, True)

Vtero.VerboseLevel = 1

# False: not a bitmap scan, True: Cloud Scan
vtero.HashAllProcs(mdb, False, True)

print "Done! Total runtime: " + TotalRunTime.Elapsed.ToString()


