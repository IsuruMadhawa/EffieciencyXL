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
                    "(id, username, email, role, hashed_password) "
                    "VALUES (%s, %s, %s, %s, %s)")
        data_user = (user.id, user.username, user.email, user.role, user.hashed_password)
        cursor.execute(add_user, data_user)
        self.cnx.commit()
        cursor.close()

    def get_user_by_username(self, username: str) -> UserInDB | None:
        cursor = self.cnx.cursor()
        query = ("SELECT id, username, email, role, hashed_password "
                 "FROM users "
                 "WHERE username = %s")
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return UserInDB(**dict(zip(['id', 'username', 'email', 'role', 'hashed_password'], row)))

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

    def insert_video_data(self, label, location, misc, img):
        """
        Add video data to the database
        Args:
            label:
            location:
            timestamp:
            misc:
            img: image bytes

        Returns:
            "Inserted successfully" if the data was inserted successfully
            An error message if the data was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO feeddata (label, location, timestamp, misc, img) "
                     "VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)")
            values = (label, location, misc, img)
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

    def insert_clearance_request(self, name, division, district, description, email):
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
            query = ("INSERT INTO clearance_requests (name, division, district, description, state, timestamp, c_email) "
                     "VALUES (%s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP, %s)")
            values = (name, division, district, description, email)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Request for clearance is sent"
        except mysql.connector.Error as err:
            print(err)
            return err

    def insert_lost_item_report(self, name, division, district, item, description):
        """
        Add a lost item report to the database
        Args:
            name: name of the civilian
            division: police division
            district: district
            item: the lost item
            description: description of the lost item

        Returns:
            "Lost item report is sent" if the report was inserted successfully
            An error message if the report was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO lost_item_reports (name, division, district, item, description, state, timestamp) "
                     "VALUES (%s, %s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)")
            values = (name, division, district, item, description)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Lost item report is sent"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_all_clearance_requests(self):
        """
        Query the clearance_requests table for all requests
        Returns:
        A list of tuples containing the data for the requests
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM clearance_requests"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def insert_complaint(self, name, division, district, complaint):
        """
        Add a complaint to the database
        Args:
            name: name of the civilian
            division: police division
            district: district
            complaint: the complaint

        Returns:
            "Complaint is sent" if the complaint was inserted successfully
            An error message if the complaint was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO complaints (name, division, district, complaint, state, timestamp) "
                     "VALUES (%s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)")
            values = (name, division, district, complaint)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Complaint is sent"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_all_lost_item_reports(self):
        """
        Query the lost_item_reports table for all reports
        Returns:
        A list of tuples containing the data for the reports
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM lost_item_reports"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_single_clearance_request(self, r_id):
        """
        Query the clearance_requests table for a specific request
        Args:
            r_id: the id of the request
        Returns:
        A list of tuples containing the data for the request
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM clearance_requests WHERE id = %s"
            cursor.execute(query, (r_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_criminal_sightings(self, name):
        """
        Query the feeddata table for all sightings of a criminal
        Args:
            name: the name of the criminal
        Returns:
        A list of tuples containing the data for the sightings
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT label, location, timestamp, misc FROM feeddata WHERE label = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def insert_new_criminal(self, name, age, description, division, district):
        """
        Add a criminal to the database
        Args:
            name: name of the criminal
            age: age of the criminal
            description: description of the criminal
            division: police division
            district: district

        Returns:
        "Criminal is added" if the criminal was inserted successfully
        An error message if the criminal was not inserted successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("INSERT INTO criminals (name, age, description, division, district) "
                     "VALUES (%s, %s, %s, %s, %s)")
            values = (name, age, description, division, district)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Criminal is added"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_all_criminals(self):
        """
        Query the criminals table for all criminals
        Returns:
        A list of tuples containing the data for the criminals
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM criminals"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def update_disapprove_clearance_report(self, r_id, o_id, details):
        """
        Update the clearance report in the database
        Args:
            r_id: the id of the request
            o_id: the id of the officer
            details: details of the report
        Returns:
        "Updated successfully" if the report was updated successfully
        An error message if the report was not updated successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("UPDATE clearance_requests "
                     "SET officer_id = %s, details = %s, state = 'disapproved', approved_timestamp = CURRENT_TIMESTAMP "
                     "WHERE id = %s")
            values = (o_id, details, r_id)
            print(values)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Updated successfully"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_all_complaints(self):
        """
        Query the complaints table for all complaints
        Returns:
        A list of tuples containing the data for the complaints
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM complaints"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def update_approve_clearance_report(self, r_id, o_id, details):
        """
        Update the clearance report in the database
        Args:
            r_id: the id of the request
            o_id: the id of the officer
            details: details of the report
        Returns:
        "Updated successfully" if the report was updated successfully
        An error message if the report was not updated successfully
        """
        try:
            cursor = self.cnx.cursor()
            query = ("UPDATE clearance_requests "
                     "SET officer_id = %s, details = %s, state = 'approved', approved_timestamp = CURRENT_TIMESTAMP "
                     "WHERE id = %s")
            values = (o_id, details, r_id)
            cursor.execute(query, values)
            self.cnx.commit()
            cursor.close()
            return "Updated successfully"
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_officer_id(self, u_id):
        """
        Query the officer_id from the users table
        Args:
            u_id: the id of the user
        Returns:
        The officer_id
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT officer_id FROM officer WHERE user_id = %s"
            cursor.execute(query, (u_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_officer_for_division(self, division):
        """
        Query the officer_id from the users table
        Args:
            division: the division
        Returns:
        The officer_id
        """
        try:
            cursor = self.cnx.cursor()
            query = "SELECT officer_id FROM officer WHERE division = %s"
            cursor.execute(query, (division,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def query_alerts(self):
        try:
            cursor = self.cnx.cursor()
            query = "select id, label, location, timestamp , misc from feeddata where alerts=0 ORDER by timestamp"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err

    def set_alert_off(self, label):
        try:
            cursor = self.cnx.cursor()
            query = "update feeddata set alerts=1 where label=%s"
            cursor.execute(query, (label, ))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return err
