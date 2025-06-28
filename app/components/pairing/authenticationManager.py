from serverEvents import *
from time import sleep

def is_paired(server, ip_address):
    ans=False
    sid=server.find_request_sid(ip_address)
    counter=0
    while ans != True:
        sleep(0.25)
        ans=server.sid_dictionary[sid].is_paired
        if counter == 30:
            break
        counter += 1
    return ans

def is_auth(server, ip_address):
    ans=False
    sid=server.find_request_sid(ip_address)
    counter=0
    while ans != True:
        sleep(0.25)
        ans=server.sid_dictionary[sid].is_auth
        if counter == 30:
            break
        counter += 1
    return ans