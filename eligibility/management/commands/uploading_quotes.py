import openpyxl as xl
from django.core.management.base import BaseCommand, CommandError
from eligibility.models import Quote

wb = xl.load_workbook('quotes.xlsx', data_only=True, read_only=True)

ws = wb.active

class Command(BaseCommand):

    def handle(self, *args, **options):

        Quote.objects.all().delete()
        data = []

        x=0
        print('reading file and uploading to database')
        for row in ws.iter_rows(row_offset=1):
            x+=1
            x_row = [cell.value for cell in row]
            quote = Quote(text=x_row[0], author=x_row[1])
            data.append(quote)
            if x%20000==0:
                print(x)

        num_rows = len(data)

        i=0

        while i*999<=num_rows:
            Quote.objects.bulk_create(data[i*999:(i+1)*999])
            i+=1
            print((i+1)*999)


        print('There are {0} quotes.'.format(num_rows))
            

