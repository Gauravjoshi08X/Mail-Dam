import psycopg2
import dotenv, os

dotenv.load_dotenv("src/certs/credential.env")

class DatabaseInsert():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")
	@staticmethod
	def insertUserData(self, email: str, uname: str, refresh_token: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO users (email, uname, refresh_token)
				VALUES (
					%s,%s,%s
				);"""
				cur.execute(event_query, (email, uname, refresh_token))
				conn.commit()

	def insertPRJData(self, project: str, user: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO project (project_name, user_id)
				VALUES (
					%s,%s
				);"""
				cur.execute(event_query, (project, DatabaseFKFetch().fetchUserFKData(user)))
				conn.commit()

	def insertOpenEventData(self, event_time: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO event (email_id, project_id, event_time, open)
				VALUES (
					%s,%s,%s
				);"""
				cur.execute(event_query, (DatabaseFKFetch().fetchFKData("email_id", "email"), DatabaseFKFetch().fetchFKData("project_id", "project"), event_time, True))
				conn.commit()

	def insertEventData(self, location: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""UPDATE event
				set click=%s, location=%s
				WHERE email_id=%s;"""
				cur.execute(event_query, (True, location))
				conn.commit()

	def insertEmailData(self, recipient: str, subject: str, sent_at: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO email (project_id, recipient_email, subject, sent_at)
				VALUES (
					%s,%s,%s,%s
				);"""
				cur.execute(event_query, (DatabaseFKFetch().fetchFKData("project_id", "project"), recipient, subject, sent_at))
				conn.commit()

class DatabaseFKFetch():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")

	def fetchFKData(self,id: str, table: str) -> int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query=f"""SELECT MAX({id}) FROM {table};"""
				cur.execute(event_query)
				result=cur.fetchone()
				return result[0]

	def fetchUserFKData(self, uname: str)->int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""SELECT user_id FROM users where uname=%s;"""
				cur.execute(event_query, (uname,))
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

	def fetchEmailData(self,user: str) -> str:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""SELECT email from users where uname=%s"""
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
