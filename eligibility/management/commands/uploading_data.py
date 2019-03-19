import openpyxl as xl
from django.core.management.base import BaseCommand, CommandError
from eligibility.models import GovEmployee

wb = xl.load_workbook('Final_Product.xlsx', data_only=True, read_only=True)

ws = wb.active

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('clearing database')
        GovEmployee.objects.all().delete()
        print('done clearing database')

        print('There are {0} employees.'.format(GovEmployee.objects.all().count()))
        data = []

        x=0
        print('reading file and uploading to database')
        for row in ws.iter_rows(row_offset=1):
            x+=1
            x_row = [cell.value for cell in row]
            emp = GovEmployee(emp_id = x_row[0], full_name = x_row[1], dob = x_row[2],
                              assignment_status = x_row[3], gender = x_row[4],
                              job = x_row[5], organization = x_row[6],
                              hire_date = x_row[7], department = x_row[8],
                              ministry = x_row[9], ssn = x_row[10],
                              bank_name = x_row[11], bank_branch = x_row[12],
                              location = x_row[13], district = x_row[14],
                              region = x_row[15], ssn_exempt = x_row[16],
                              pupil_teacher_status = x_row[17],
                              teacher_trainee_status = x_row[18],phoneNumber = x_row[19],
			      phoneNumber2 = x_row[20],blacklisted = x_row[21])

            data.append(emp)
            if x%20000==0:
                print(x)

        num_rows = len(data)

        i=0

        while i*999<=num_rows:
            GovEmployee.objects.bulk_create(data[i*999:(i+1)*999])
            i+=1
            print((i+1)*999)


        print('There are {0} employees in the database.'.format(num_rows))
            

