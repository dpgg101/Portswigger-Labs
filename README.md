# Portswigger-Labs
## [Lab: Blind SQL injection with conditional responses](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)
Usage:
```bash
$ python3 blind-sql-trackingid.py
                                                                          
usage: blind-sql-trackingid.py [-h] --url URL

Blind SQL injection with conditional responses

options:
  -h, --help  show this help message and exit
  --url URL   URL of the target
```
Requirements:
- requests
- argparse
- string

[Exploit](https://github.com/dpgg101/Portswigger-Labs/blob/main/blind-sqli-trackingid.py)

---

## [Lab: Blind SQL injection with conditional errors](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors)

Usage:
```bash
$ python3 blind-error-based-trackingid.py                                                                     
usage: blind-error-based-trackingid.py [-h] --url URL

Blind SQL injection with conditional errors

options:
  -h, --help  show this help message and exit
  --url URL   URL of the target
```
[Exploit](https://github.com/dpgg101/Portswigger-Labs/blob/main/blind-error-based-trackingid.py)
