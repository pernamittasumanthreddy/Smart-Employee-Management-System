import os
import sys

import django

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

urls = [
    '/auth/dashboard/',
    '/employees/',
    '/employees/directory/',
    '/attendance/my-attendance/',
    '/attendance/department-summary/',
    '/leave/my-leaves/',
    '/leave/apply/',
    '/leave/approvals/',
    '/leave/calendar/',
    '/shifts/',
    '/shifts/holidays/',
    '/workload/',
    '/projects/',
    '/tasks/',
    '/tasks/kanban/',
    '/skills/catalog/',
    '/skills/matrix/',
    '/goals/my-goals/',
    '/performance/cycles/',
    '/training/',
    '/recognition/',
    '/recognition/leaderboard/',
    '/assets/',
    '/assets/my-assets/',
    '/expenses/',
    '/expenses/approvals/',
    '/helpdesk/',
    '/helpdesk/my-tickets/',
    '/documents/',
    '/documents/my-documents/',
    '/announcements/',
    '/announcements/events/',
    '/notifications/',
    '/insights/',
    '/reports/',
]

if __name__ == '__main__':
    for uname in ['priya.patel', 'hrmanager', 'rajesh.kumar', 'manager', 'sneha.iyer', 'employee', 'aarav.sharma', 'admin']:
        c = Client()
        ok = c.login(username=uname, password='Admin@12345')
        print("\n==================================================")
        print(f"Testing User: {uname} (Login Success: {ok})")
        print("==================================================")
        for u in urls:
            resp = c.get(u, follow=False)
            loc = resp.get('Location', '')
            if resp.status_code == 200:
                print(f"  [200 OK] {u}")
            elif resp.status_code in (301, 302):
                print(f"  [{resp.status_code} Redirect] {u} -> {loc}")
            else:
                print(f"  [{resp.status_code} ERROR/FORBIDDEN] {u}")
