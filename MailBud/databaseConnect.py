import psycopg2
import dotenv, os

dotenv.load_dotenv("src/certs/credential.env")
class DatabaseInsert():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")
		self.fetchpk=DatabasePKFetch()

	def insertUserData(self, email: str, uname: str, refresh_token: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""INSERT INTO users (email, uname, refresh_token)
				VALUES (
					%s,%s,%s
				);"""
				cur.execute(event_query, (email, uname, refresh_token))
				conn.commit()

	def insertPRJData(self, project: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""INSERT INTO project (project_name, user_id)
				VALUES (
					%s,%s
				);"""
				cur.execute(event_query, (project, self.fetchpk.fetchFKData("user_id", "users")))
				conn.commit()

	def insertEventData(self, location: str, useragent: str, event_time: str, opened: str, click: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""INSERT INTO project (email_id, location, user_agent, event_time, open, click)
				VALUES (
					%s,%s,%s,%s,%s,%s
				);"""
				cur.execute(event_query, (self.fetchpk.fetchFKData("email_id", "email"), location, useragent, event_time, opened, click))
				conn.commit()

	def insertEmailData(self, recipient: str, subject: str, sent_at: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""INSERT INTO project (project_id, recipient, subject, sent_at)
				VALUES (
					%s,%s,%s,%s
				);"""
				cur.execute(event_query, (self.fetchpk.fetchFKData("project_id", "project"), recipient, subject, sent_at))
				conn.commit()
T
class DatabasePKFetch():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")

	def fetchFKData(self,id, table) -> int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""SELECT MAX({id}) FROM {table}"""
				cur.execute(event_query)
				result=cur.fetchone()
				return result[0]+1
