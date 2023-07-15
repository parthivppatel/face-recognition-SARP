import mysql.connector


try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        # database="face_rec",
        password="root",
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    if connection.is_connected():
        print("Connected to MySQL database!")
    # SQL command to create a new database
    create_db_query = "CREATE DATABASE face_data;"

    # Execute the SQL command
    cursor.execute(create_db_query)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    print("Database created successfully!")

except mysql.connector.Error as error:
    print("Error while connecting to MySQL:", error)
