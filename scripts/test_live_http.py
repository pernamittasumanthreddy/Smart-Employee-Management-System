import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Fetch Login Page
resp = opener.open('http://127.0.0.1:8000/auth/login/')
html = resp.read().decode('utf-8')
token_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html)
token = token_match.group(1) if token_match else ''
print(f"1. Login Page: HTTP {resp.status}, CSRF Token extracted: {bool(token)}")

# 2. Submit Login Credentials
post_data = urllib.parse.urlencode({
    'username': 'aarav.sharma',
    'password': 'Admin@12345',
    'csrfmiddlewaretoken': token
}).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:8000/auth/login/',
    data=post_data,
    headers={'Referer': 'http://127.0.0.1:8000/auth/login/'}
)
resp_login = opener.open(req)
print(f"2. Login Submit: HTTP {resp_login.status} -> Redirected to: {resp_login.geturl()}")

# 3. Access Dashboard
resp_dash = opener.open('http://127.0.0.1:8000/auth/dashboard/')
print(f"3. Dashboard Load: HTTP {resp_dash.status} -> Final URL: {resp_dash.geturl()}")

# 4. Access Payroll
resp_pay = opener.open('http://127.0.0.1:8000/payroll/')
print(f"4. Payroll Dashboard Load: HTTP {resp_pay.status} -> Final URL: {resp_pay.geturl()}")

# 5. Access Recruitment
resp_rec = opener.open('http://127.0.0.1:8000/recruitment/')
print(f"5. Recruitment Pipeline Load: HTTP {resp_rec.status} -> Final URL: {resp_rec.geturl()}")

print("\nSUCCESS: All live HTTP requests completed with HTTP 200 OK!")
