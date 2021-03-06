#
#
# To debug you can try like so;
# ipy64 -X:TabCompletion -X:ShowClrExceptions -X:PrivateBinding -X:PassExceptions -X:FullFrames -X:Frames -X:ExceptionDetail -D
#
#

import clr

clr.AddReferenceToFileAndPath("inVtero.net.dll")
clr.AddReferenceToFileAndPath("inVtero.net.ConsoleUtils.dll")

from inVtero.net import *
from inVtero.net.ConsoleUtils import *
from System.IO import Directory, File, FileInfo, Path
from System import ConsoleColor, Console, Environment, Char, String
from System.Text import Encoding


def AssignProc(v, p):
    p.MemAccess = Mem(v.MemAccess)
    pt = PageTable.AddProcess(p, p.MemAccess)
    p.KernelSection = v.KernelProc.KernelSection
    p.CopySymbolsForVad(v.KernelProc)
    p.ID = v.KernelProc.ID
    p.sym = v.KernelProc.sym



def GetProc(v, str, prev = None):
    SeenPrev = False
    if prev is None:
        SeenPrev = True
    for p in v.Processes.ToArray():
        if prev is not None and prev.CR3Value == p.CR3Value:
            SeenPrev = True
        if p.OSFileName is not None:
            if p.OSFileName.lower().Contains(str.lower()):
                AssignProc(v, p)
                return p


# Display Symbols
def ds(p, addr, len=128, maxWid = 72):
    if Console.WindowWidth-4 < maxWid:
        maxWid = Console.WindowWidth-4
    words = p.GetVirtualLongLen(addr, len)
    len = len / 8
    curr = 0
    while curr < len:
        Misc.WxColor(ConsoleColor.White, ConsoleColor.Black, VIRTUAL_ADDRESS(addr+(curr*8)).xStr + " ")
        Misc.WxColor(ConsoleColor.Green, ConsoleColor.Black, words[curr].ToString("x16") + " ")
        Misc.WxColor(ConsoleColor.Cyan, ConsoleColor.Black, "[" +  p.GetSymName(words[curr]) + "]")
        curr = curr+1
        Console.Write(Environment.NewLine);

# Display quadwords
def dq(p, addr, len=128, maxWid = 72):
    if Console.WindowWidth-4 < maxWid:
        maxWid = Console.WindowWidth-4
    words = p.GetVirtualLongLen(addr, len)
    len = len / 8
    curr = 0
    while curr < len:
        Misc.WxColor(ConsoleColor.White, ConsoleColor.Black, VIRTUAL_ADDRESS(addr+(curr*8)).xStr + " ")
        while curr < len and Console.CursorLeft < maxWid:
            Misc.WxColor(ConsoleColor.Green, ConsoleColor.Black, words[curr].ToString("x16") + " ")
            curr = curr+1
        Console.Write(Environment.NewLine);

# Display bytes
def db(p, addr, len=128, bytesPerLine = 16):
    words = p.GetVirtualByteLen(addr, len)
    curr = 0
    while curr < len:
        Misc.WxColor(ConsoleColor.White, ConsoleColor.Black, VIRTUAL_ADDRESS(addr+curr).xStr + " ")
        for c in range(0, bytesPerLine):
            Misc.WxColor(ConsoleColor.Green, ConsoleColor.Black, words[curr+c].ToString("x2") + " ")
        for ch in range(0, bytesPerLine):
            myChar = Encoding.ASCII.GetString(words, curr+ch,1)[0]
            if Char.IsLetterOrDigit(myChar) == False:
                myChar = " "
            Misc.WxColor(ConsoleColor.Cyan, ConsoleColor.Black, myChar + " ")
        Console.Write(Environment.NewLine)
        curr = curr + bytesPerLine





