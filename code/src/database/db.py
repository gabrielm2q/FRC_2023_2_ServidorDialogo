import psycopg2 as pg
from enum import Enum

class chat_type(Enum):
  keyboard_only = 1
  webcam_only = 2
  keyboard_webcam = 3

class userParams:
  id = None
  username = None
  password = None
  chat_type: chat_type | None = None

class db:
  def __init__(self):
    self.db = pg.connect("dbname=chat user=frc password=\'123123\'")
    self.cursor = self.db.cursor()

  def select_all(self, params: userParams):
    if params.username:
      sql = f"SELECT * FROM users WHERE username=%s;"
      self.cursor.execute(sql, (params.username))
    
    self.db.commit()

  def insert_one(self, params: userParams):
    if params.username and params.password and params.chat_type:
      sql = f"INSERT INTO users(username, password, chat_type) VALUES (%s, %s, %s);"
      self.cursor.execute(sql, (params.username, params.password, params.chat_type))
    
    self.db.commit()

  def update_one(self, params: userParams):
    if params.username:
      sql = f"UPDATE users SET username=%s WHERE id=%s;"
      self.cursor.execute(sql, (params.username, params.id))
    if params.password:
      sql = f"UPDATE users SET password=%s WHERE id=%s;"
      self.cursor.execute(sql, (params.password, params.id))
    if params.chat_type:
      sql = f"UPDATE users SET chat_type=%s WHERE id=%s;"
      self.cursor.execute(sql, (params.chat_type, params.id))

    self.db.commit()
  
  def delete_one(self, params: userParams):
    if params.id:
      sql = f"DELETE FROM users WHERE id=%s;"
      self.cursor.execute(sql, (params.id))
    
    self.db.commit()