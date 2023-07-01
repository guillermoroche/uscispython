import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="48931394k$",
  database="uscis"
)

mycursor = mydb.cursor()

#sql = "INSERT INTO aos (name, address) VALUES (%s, %s)"
#val = ('WAC', '2390020087', 'I-765', 'delivered', '2023/01/23')
sql = "INSERT INTO aos (`usciscenter`, `casenumber`, `form`, `datefiled`, `status`) VALUES ('WAC', '0123456789', 'I-393', '1993/08/17', 'APPROVED')"
mycursor.execute(sql)
#mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")