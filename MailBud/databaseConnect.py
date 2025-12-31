import psycopg2
def insertData(location: str|None, device: str|None, UA: str|None, event_time: str|None) -> None:
	conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")

	cur=conn.cursor()

	event_query=f"""INSERT INTO event (
	    location,
	    user_agent,
	    event_time
	  )
	VALUES (
	    {location},
	    {UA},
	    {event_time}
	  );"""

	cur.execute(event_query)