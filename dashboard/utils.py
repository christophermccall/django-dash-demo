import csv
from django.conf import settings

def is_non_profit_ein(ein):
    ein_file_path = settings.BASE_DIR / 'dashboard/static/data/irs_nonprofits.csv'
    
    try:
        with open(ein_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0].strip() == ein:
                    return True
    except FileNotFoundError:
        print("IRS Non-Profit EIN CSV not found.")
    return False