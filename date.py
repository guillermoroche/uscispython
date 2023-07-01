from datetime import datetime

date_string_1 = "June 14, 2023"
format_1 = '%B %d, %Y'
date_string_1 = date_string_1.replace(',', '', 1)
print(date_string_1)
#date_1 = datetime.strptime(date_string_1, format_1)
#print(date_1)