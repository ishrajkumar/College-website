import mysql.connector
conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="college_db"
        )

cursor = conn.cursor()

query ="INSERT INTO users(email, password) VALUES(%s, %s)"
values = ("ik@gmail.com", "test_password")

cursor.execute(query, values)
conn.commit()
print("User Inserted Succesfully!")

cursor.close()
conn.close()

