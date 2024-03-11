from datetime import datetime

import mysql.connector
from mysql.connector import errorcode

from models.user_model import User, UserInDB

"""
    middleware for accessing the user database and performing CRUD operations on the user table
"""


class UserDAO:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnx = None

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def disconnect(self):
        if self.cnx is not None:
            self.cnx.close()

    def create_user(self, user: User):
        cursor = self.cnx.cursor()
        add_user = ("INSERT INTO users "
                    "(id, username, email, is_admin, hashed_password) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_user = (user.id, user.username, user.email, user.is_admin, user.hashed_password)
        cursor.execute(add_user, data_user)
        self.cnx.commit()
        cursor.close()

    def get_user_by_username(self, username: str) -> UserInDB | None:
        cursor = self.cnx.cursor()
        query = ("SELECT id, username, email, is_admin, hashed_password "
                 "FROM users "
                 "WHERE username = %s")
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return UserInDB(**dict(zip(['id', 'username', 'email', 'is_admin', 'hashed_password'], row)))

    def get_last_user_id(self) -> int:
        cursor = self.cnx.cursor()
        query = "SELECT MAX(id) FROM users"
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return 0
        return row[0]

    def blacklist_token(self, token: str):
        """
        Add a token to the blacklist table with the current timestamp
        """
        try:
            cursor = self.cnx.cursor()
            query = "INSERT INTO blacklist (token, blacklisted_on) VALUES (%s, %s)"
            timestamp = datetime.now()
            values = (token, timestamp)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(err)

    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if a token exists in the blacklist table
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT COUNT(*) FROM blacklist WHERE token = %s"
            values = (token,)
            cursor.execute(query, values)
            result = cursor.fetchone()[0]
            cursor.close()
            return result > 0
        except mysql.connector.Error as err:
            print(err)
            return False

    def insert_video_data(self, label, location, timestamp, misc):
        """
        Add video data to the database
        Args:
            label:
            location:
            timestamp:
            misc:

        Returns:
            "Inserted successfully" if the data was inserted successfully
            An error message if the data was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO feeddata (label, location, timestamp, misc) "
                     "VALUES (%s, %s, CURRENT_TIMESTAMP, %s)")
            values = (label, location, timestamp, misc)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Inserted successfully"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_feeddata_for_name(self, name):
        """
        Query the feeddata table for a specific name
        Args:
            name: the name to query for

        Returns:
            A list of tuples containing the data for the name
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM feeddata WHERE label = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def insert_clearance_request(self, name, division, district, description):
        """
        Add a clearance request to the database
        Args:
            name: name of the civilian
            division: police division
            district: district
            description: description of the request

        Returns:
            "Request for clearance is sent" if the request was inserted successfully
            An error message if the request was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO clearance_requests (name, division, district, description, timestamp) "
                     "VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)")
            values = (name, division, district, description)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Request for clearance is sent"
        except mysql.connector.Error as err:
            print(err)
            return err
