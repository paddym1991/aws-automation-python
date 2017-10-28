#!/usr/bin/env python3

"""A tiny Python program to check that nginx is running.
Try running this program from the command line like this:
  python3 check_webserver.py
"""

import sys
import subprocess


def start_nginx():
    cmd = 'ps -A | grep nginx'

    (status, output) = subprocess.getstatusoutput(cmd)

    if status == 0:
        print("Nginx server is already running")
        sys.exit(1)
    else:
        sys.stderr.write(output)
        print("Nginx Server not running, so let's try to start it now...")
        cmd = 'sudo service nginx start'
        (status, output) = subprocess.getstatusoutput(cmd)
        if status:
            print("--- Error starting nginx! ---")
            sys.exit(2)
        print("Nginx started successfully")
        sys.exit(0)


def check_nginx():
    cmd = 'ps -A | grep nginx | grep -v grep'

    (status, output) = subprocess.getstatusoutput(cmd)

    if status > 0:  
        print("Nginx Server IS NOT running")
        start_nginx()
    else:
        print("Nginx Server IS running")


# Define a main() function.
def main():
    check_nginx()


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

