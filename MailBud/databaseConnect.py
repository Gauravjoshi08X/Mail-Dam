import psycopg2
import dotenv, os

dotenv.load_dotenv("src/certs/credential.env")
name=os.getenv("DBNAME")
user=os.getenv("DBUSER")
password=os.getenv("DBPASSWORD")

class DatabaseInsert():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")
		self.fetchpk=DatabasePKFetch()
	@staticmethod
	def insertUserData(email: str, uname: str, refresh_token: str) -> None:
		with psycopg2.connect(f"dbname={name} user={user} password={password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO users (email, uname, refresh_token)
				VALUES (
					%s,%s,%s
				);"""
				cur.execute(event_query, (email, uname, refresh_token))
				conn.commit()

	def insertPRJData(self, project: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO project (project_name, user_id)
				VALUES (
					%s,%s
				);"""
				cur.execute(event_query, (project, self.fetchpk.fetchFKData("user_id", "users")))
				conn.commit()

	def insertEventData(self, location: str, useragent: str, event_time: str, opened: str, click: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO project (email_id, location, user_agent, event_time, open, click)
				VALUES (
					%s,%s,%s,%s,%s,%s
				);"""
				cur.execute(event_query, (self.fetchpk.fetchFKData("email_id", "email"), location, useragent, event_time, opened, click))
				conn.commit()

	def insertEmailData(self, recipient: str, subject: str, sent_at: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO project (project_id, recipient, subject, sent_at)
				VALUES (
					%s,%s,%s,%s
				);"""
				cur.execute(event_query, (self.fetchpk.fetchFKData("project_id", "project"), recipient, subject, sent_at))
				conn.commit()

class DatabasePKFetch():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")

	def fetchFKData(self,id, table) -> int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""SELECT MAX({id}) FROM {table}"""
				cur.execute(event_query, (id, table))
				result=cur.fetchone()
				return result[0]

class DatabaseFetch():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")

	def isUser(self, user: str)-> bool:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				user_query="""
				select exists(select 1 from users where uname=%s)
				"""
				cur.execute(user_query, (user,))
				result=cur.fetchone()
				return result[0]

	def fetchRTData(self,user) -> str:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""SELECT refresh_token from users where uname=%s"""
				cur.execute(event_query, (user,))
				result=cur.fetchone()
				return result[0]

	def fetchStat(self, user: str) -> list[tuple]:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""
				select count(open), count(click) from event where project_id=(select max(project_id) from project where user_id=(select user_id from users where uname=%s;));
				"""
				cur.execute(event_query, (user,))
				result=cur.fetchone()
				return result
