# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=4>

# From python library [concurrent.futures](https://docs.python.org/3.3/library/concurrent.futures.html)

# <codecell>

import subprocess
simulation = subprocess.Popen(['ping', 'google.com', '-n','10'], stdout=subprocess.PIPE)
output = []
while simulation.poll() is None:
    l = simulation.stdout.readline().decode("utf-8").strip() # This blocks until it receives a newline.
    if l:
        print(l)
        output.append(l)
print( simulation.stdout.read().decode("utf-8"))
# When the subprocess terminates there might be unconsumed output 
# that still needs to be processed.
# print(output)

# <codecell>

import re
cmd_string = 'Reply from 74.125.225.161: bytes=32 time=24ms TTL=55'
ip, bytes, time, ignore =  re.sub(r'Reply from |bytes=|ms|time=|:', '', cmd_string).split()
print(ip, bytes, time, ignore)

# <codecell>


# <codecell>

import os
os.startfile('sqlite3.exe')

# <codecell>

command = 'sqlite3.exe --help'
os.system(command)

# <codecell>

import subprocess
import sys
command = ['sqlite3.exe', '--help']
child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
for x in range(10000):
    out = child.stdout.read(1)
    if out == '' and child.poll() != None:
        break
    if out:
        print(out)
#         sys.stdout.flush()

# <codecell>

proc = subprocess.Popen('sqlite3.exe --help', shell=True, stdout=subprocess.PIPE)
try:
    outs, errs = proc.communicate(timeout=15)
except subprocess.TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
print(outs, errs)

# <headingcell level=1>

# This actually works:

# <codecell>

subprocess.check_output(['ipconfig'])

# <headingcell level=2>

# TODO: check try subprocess.communicate()

# <codecell>


# <codecell>

import threading
import datetime
import time

class TestThread(threading.Thread):
    def run(self):
        while True:
            print(datetime.datetime.now(), threading.current_thread() )
            time.sleep(1)
    
    def call_me(self):
        print("I'm",  threading.current_thread())
    

# <codecell>

threading.current_thread()

# <codecell>

t = TestThread()
t.start()

# <codecell>

t.call_me()

# <codecell>


# <codecell>

import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://newline.us/']

# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    conn = urllib.request.urlopen(url, timeout=timeout)
    return conn.readall()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))

# <markdowncell>

# Works because Threads are interactive.

# <codecell>


# <codecell>

import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

main()

# <markdowncell>

# Doesn't work because multiprocessing library is not interactive.

# <codecell>


# <codecell>

# <markdowncell>

# Doesn't work because I haven't set up security.

# <markdowncell>

# 
# 
# 
# 

# <codecell>


# <codecell>

import subprocess
import sys

cmd = 'ipconfig'
def pipe_test():
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    while True:
        out = process.stdout.read(1)
        if out == '' :#and process.poll() != None
            break
        if out != '':
            print(out)
#             sys.stdout.flush()
            

# <codecell>


