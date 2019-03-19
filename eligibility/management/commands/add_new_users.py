import openpyxl as xl
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

class Command(BaseCommand):

    def handle(self, *args, **options):
        auth_password = 'D@l3xadm1n'
        wb = xl.load_workbook('new_users.xlsx', data_only=True, read_only=True)
        ws = wb.active

        for row in ws.iter_rows(row_offset=1):
            x_row = [cell.value for cell in row]
            first_name = x_row[1].strip()
            last_name = x_row[2].strip()
            email = x_row[3].strip()
            username = email.split('@')[0]
            password = User.objects.make_random_password()
            User.objects.create_user(username=username,
                                     first_name=first_name,
                                     last_name=last_name,
                                     email=email,
                                     password=password)
            

            send_mail(
                'Eligibility Login Credentials',
                ('Hello {0}, \n\nYour username is: {1}.\n\n'
                 'Your password is: {2}.\n\n'
                 'Please login at this URL: '
                 'http://www.dalexhq.com').format(first_name, username,
                                                  password),
                'tech@dalexfinance.com',
                [email],
                auth_user = 'tech@dalexfinance.com',
                auth_password = auth_password
                )
            

