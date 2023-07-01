import requests
from datetime import datetime
import time

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="48931394k$",
  database="uscis"
)
mycursor = mydb.cursor()

base_url = "https://egov.uscis.gov/csol-api/case-statuses/WAC"

case_number = 2390050000

format_1 = '%B %d %Y'

i = 0
cases = []
while i<1000:
    time.sleep(0.25)
    print(base_url+str(case_number+i))
    resp = requests.get(base_url+str(case_number+i))
    if (resp.json()["CaseStatusResponse"]["isValid"] == True):
        if resp.json()["CaseStatusResponse"]["detailsEng"]["formNum"] == 'I-765' or \
           resp.json()["CaseStatusResponse"]["detailsEng"]["formNum"] == 'I-485' or \
           resp.json()["CaseStatusResponse"]["detailsEng"]["formNum"] == 'I-131' :
            status = ""
            #*********************DATE PROCESSING**************************************************
            if resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeDesc"][:2] == 'On':
                desc_date = resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeDesc"][3:25]
            else:
                desc_date = resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeDesc"][6:30]
            desc_date = ""
            desc_date = desc_date.replace(',', '', 1)
            desc_date = desc_date[:desc_date.find(",")]
            try:
                desc_date = datetime.strptime(desc_date, format_1).date()
            except:
                print("No date found")

            
            #**************************************************************************************
            if 'Rejected' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "REJECTED"
            if 'Case Was Received' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "RECEIVED"
            if 'Case Was Approved' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or \
               'Card Was Picked Up By The United States Postal Service' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or\
               'Case Closed Benefit Received By Other Means' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or \
               'Card Was Delivered To Me By The Post Office' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "APPROVED"
            if 'Request for Initial Evidence Was Sent' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or \
                'Request for Additional Evidence Was Sent' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or\
                'Request For Evidence Was Received' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "RFE"
            if 'Case Was Updated To Show Fingerprints Were Taken' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"] or\
               'Fingerprint Fee Was Received' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "BIOMET"
            if 'Case Was Denied' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "DENIED"
            if 'Case Was Transferred And A New Office Has Jurisdiction' in resp.json()["CaseStatusResponse"]["detailsEng"]["actionCodeText"]:
                status = "TRANSFER"
            #**************************************************************************************
            if status == "REJECTED" or \
               status == "APPROVED" or \
               status == "DENIED" or \
               status == "TRANSFER":
                newline = ('WAC', str(case_number+i), \
                       resp.json()["CaseStatusResponse"]["detailsEng"]["formNum"], \
                       status, \
                       "",\
                       str(desc_date))
            else:
                newline = ('WAC', str(case_number+i), \
                       resp.json()["CaseStatusResponse"]["detailsEng"]["formNum"], \
                       status, \
                       str(desc_date), \
                        "")
            cases.append(newline)
            #**************************************************************************************
    else:
        print("No existe")
    i = i+1
print (*cases, sep="\n")
sql = "INSERT INTO aos (`usciscenter`, `casenumber`, `form`, `status`,`datefiled`,`datefinished`) VALUES (%s, %s, %s, %s, %s,%s)"
mycursor.executemany(sql,cases)

mydb.commit()