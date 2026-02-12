import psycopg2
import dotenv, os

dotenv.load_dotenv("src/certs/credential.env")

class DatabaseInsert():
	def __init__(self):
		self.name=os.getenv("DBNAME")
		self.user=os.getenv("DBUSER")
		self.password=os.getenv("DBPASSWORD")

	def insertUserData(self, email: str, uname: str, refresh_token: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				check_query="""SELECT EXISTS(SELECT user_id from users where email=%s)"""
				cur.execute(check_query, (email,))
				if cur.fetchone()[0]==False:
					event_query="""INSERT INTO users (email, uname, refresh_token)
					VALUES (
						%s,%s,%s
					);"""
					cur.execute(event_query, (email, uname, refresh_token))
					conn.commit()
				else:
					print(f"it's coming here\n{refresh_token}\nended")
					event_query="""UPDATE users set refresh_token=%s where email=%s"""
					cur.execute(event_query, (refresh_token, email))
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

	def insertOpenEventData(self, event_time, email: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""INSERT INTO event (email_id, project_id, event_time, open)
				VALUES (
					%s,%s,%s,%s
				);"""
				cur.execute(event_query, (DatabaseFKFetch().fetchUserEventData(email), DatabaseFKFetch().fetchFKData("project_id", "project"), event_time, True))
				conn.commit()

	def insertEventData(self, location: str, email: str) -> None:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""UPDATE event
				set click=%s, location=%s
				WHERE email_id=%s;"""
				cur.execute(event_query, (True, location, DatabaseFKFetch().fetchUserEventData(email)))
				conn.commit()

	def insertEmailData(self, recipient: str, subject: str, sent_at) -> None:
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

	def fetchUserEventData(self, email: str)->int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""SELECT email_id FROM email where recipient_email=%s;"""
				cur.execute(event_query, (email,))
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
	
	def totalEmails(self, user: str) -> int:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				event_query="""
			select count(*) from email where project_id=(select max(project_id) from project where user_id=(select user_id from users where uname=%s))
				"""
				cur.execute(event_query, (user,))
				result=cur.fetchone()
				return result[0]

	def fetchStat(self, user: str):
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				open_query="""
			select count(distinct(email_id)) from event where open is true and project_id=(select max(project_id) from project where user_id=(select user_id from users where uname=%s))
			"""
				cur.execute(open_query, (user,))
				open=cur.fetchone()
				click_query="""
				select count(distinct(email_id)) from event where click is true and project_id=(select max(project_id) from project where user_id=(select user_id from users where uname=%s))
					"""
				cur.execute(click_query, (user,))
				click=cur.fetchone()
				return (open, click)

	def location(self, user: str) -> str:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				location_query="""
			select max(location) from event where project_id=(select max(project_id) from project where user_id=(select user_id from users where uname=%s))
			"""
				cur.execute(location_query, (user,))
				location=cur.fetchone()
				return location[0]
	
	def getEmails(self, user: str) -> list:
		with psycopg2.connect(f"dbname={self.name} user={self.user} password={self.password}") as conn:
			with conn.cursor() as cur:
				email_query="""
					SELECT DISTINCT e.recipient_email
					FROM email e
					INNER JOIN event ev ON ev.email_id = e.email_id
					WHERE ev.click = true and ev.project_id=(
						SELECT MAX(project_id)
						FROM project
						WHERE user_id = (
							SELECT user_id
							FROM users
							WHERE uname = 'Gaurav Joshi'
    ))

				"""
				cur.execute(email_query, (user,))
				emails=cur.fetchall()
				return [email[0] for email in emails]

	def sendStat(self, user: str)-> dict:
		payload={
			"opened": f"{DatabaseFetch().fetchStat(user)[0][0]}/{DatabaseFetch().totalEmails(user)}",
			"clicked": f"{DatabaseFetch().fetchStat(user)[1][0]}/{DatabaseFetch().totalEmails(user)}",
			"rating": f"{Calculate().computeOpenRate(user)}",
			"ctor": f"{Calculate().CTOR(user)}%",
			"location": f"{DatabaseFetch().location(user) if DatabaseFetch().location(user) else 'No Clicks Yet'}"
		}
		return payload


class Calculate():
	def computeOpenRate(self, user: str) -> float:
		opened, _=DatabaseFetch().fetchStat(user)
		total=DatabaseFetch().totalEmails(user)
		if total==0:
			return 0.0
		return f"{(opened[0]/total)*5:.2f}"

	def CTOR(self, user: str) -> float:
		opened, clicked=DatabaseFetch().fetchStat(user)
		if opened[0]==0:
			return 0.0
		return f"{(clicked[0]/opened[0])*100:.2f}"

if __name__=="__main__":
	...