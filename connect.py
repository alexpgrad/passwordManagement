import psycopg2
import pyotp
from config import load_config
from datetime import datetime
import hashlib, string, os
from cryptography.fernet import Fernet

key = 'tBgt2RmUlzLzzHrDJjigDZY9NOmMB2ieFwM5HnvMkKo='
cipher_suite = Fernet(key)

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
#======================================Account Sign Up====================================================================

def register(username, password, config):
    """Attempt to register a new user."""
    connection = connect(config)
    if connection is None:
        return "Connection failed"
    
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "User already exists"

        # Insert new user
        salt = os.urandom(16)
        hashing = hashlib.sha256()
        hashing.update(salt + password.encode())
        hashed_password = hashing.hexdigest()
        now = datetime.now()

        #GENERATE SECRET KEY FOR EACH USER
        secretkey = pyotp.random_base32()

        cursor.execute("INSERT INTO users (username, password, created_at, last_login, salt, secretkey) VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, hashed_password, now, now, salt, secretkey))
        connection.commit()
        return "Password stored successfully!"
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        connection.close()

#======================================Password Manager Accounts====================================================================


def store_passwords(username, password, email, url, site_name, config):
    """Store new password details into the database"""
    connection = connect(config)
    cursor = connection.cursor()

    salt = os.urandom(16)
   
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    psql_insert_request = """ INSERT INTO accounts (username, password, email, url, site_name, created_at, last_login, salt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    now = datetime.now()

    insert_user_entry = (username, encrypted_password, email, url, site_name, now, now, salt) 
    cursor.execute(psql_insert_request, insert_user_entry)
    connection.commit()
    cursor.close()
    print("Password stored successfully!")

def get_all_data(config):
    connection = connect(config)
    cursor = connection.cursor()
    try: 
        cursor.execute("SELECT id, username, password, email, url, site_name, created_at, last_login FROM accounts ORDER BY id")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts found in the database.")
            return []

        print(f"Fetched {len(accounts)} accounts from the database.")
        decrypted_accounts = []

        for account in accounts:
            try:
                # Decrypt the password - ensure the password is at index 2
                decrypted_password = cipher_suite.decrypt(account[2].encode()).decode()
                print(f"Decrypted Password: {decrypted_password}")  # Printing decrypted password for debugging
                # Recreate the account tuple with decrypted password
                decrypted_account = account[:2] + (decrypted_password,) + account[3:]
                decrypted_accounts.append(decrypted_account)
            except Exception as e:
                print(f"Error decrypting password for account ID {account[0]}: {e}")

        return decrypted_accounts
    except (Exception, psycopg2.Error) as error:
        print(f"Error retrieving data: {error}")
        return []
    finally: 
        if connection is not None:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    config = load_config()
    connect(config)


