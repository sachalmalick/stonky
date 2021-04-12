import sqlite3

db_name = "events.db"

'''
:

Date,Time,Title,Contact,Link

Date(varchar 100), Time(varchar 100), Title(text), Contact(text), Link(text)creator_id(varchar 255)

'''



'''
events:

Date,Time,Title,Contact,Link

Date(varchar 100), Time(varchar 100), Title(text), Contact(text), Link(text)creator_id(varchar 255)

'''

EVENTS_TABLE = '''
	CREATE TABLE `events` (
        `event_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		`Date` VARCHAR(100),
		`Time` VARCHAR(100),
		`Title` TEXT,
		`Contact` TEXT,
		`Link` TEXT,
		`creator_id` VARCHAR(255)
	);'''

'''
execute select query, without exception handling

@param command: prepared query as a string
@return: list of rows that match query
'''
def execute_select(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	results = c.execute(command)
	l = []
	for row in results:
		l.append(row)
	conn.close()
	return l

'''
execute list of update commands, with exception handling on each one.

@param command: list of prepared queries as strings
'''
def execute_update(command):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	if(isinstance(command, list)):
		for cmd in command:
			try:
				c.execute(cmd)
			except Exception as e:
				print(str(e))
				print(cmd)
	else:
		c.execute(command)
	conn.commit()
	conn.close()

def create_event(date,time,title,contact,link, creator_id):
	statement = "INSERT INTO events (Date, Time, Title, Contact, Link, creator_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
	statement = statement.format(date, time, title, contact, link,creator_id)
	execute_update(statement)

'''
returns the value associated with the key in dic, or an empty 
string if the k,v pair is not present

@param dic: dictionary
@param key: name of the key
@return: dic[key] or val
'''
def get_key(dic, key):
	val = dic.get(key)
	if(val == None):
		return ""
	return val
	
def update_event(students, values):
	cmds = []
	for student in students:
		key_val = get_key(student, key)
		stmt = "UPDATE events SET {} = '{}' WHERE email = '{}' and org_id = '{}'"
		stmt = stmt.format(key_name, key_val, email, orgid)
		print(stmt)
		cmds.append(stmt)
	execute_update(cmds)


def get_all_events(creator_id=None):
    stmt = "SELECT * FROM events WHERE "
    if(creator_id == None):
        stmt+="1"
    else:
        stmt+="creator_id = '{}'".format(creator_id)
    events = execute_select(stmt)
    results = []
    for event in events:
        updatedv = {}
        updatedv["event_id"] = event[0]
        updatedv["Date"] = event[1]
        updatedv["Time"] = event[2]
        updatedv["Title"] = event[3]
        updatedv["Contact"] = event[4]
        updatedv["Link"] = event[5]
        updatedv["creator_id"] = event[6]
        results.append(updatedv)
    return results

def delete_event(event_id):
    stmt = "DELETE FROM events WHERE event_id = {}"
    stmt = stmt.format(event_id)
    execute_update(stmt)

'''

'''	
def create_tables():
	commands = []
	commands.append("DROP TABLE IF EXISTS events")
	commands.append(EVENTS_TABLE)
	execute_update(commands)
	
if __name__ == "__main__":
    #create_tables()
    #create_event("2021-03-21", "5pm", "Testing This", "zach seinfeld", "", "blah")
    #create_event("2021-03-21", "5pm", "Testing This", "zach seinfeld", "", "blah")
    #create_event("2021-06-03", "5pm", "Birthday Party", "zseinfel", "www.espn.com", "yo")
    #create_event("2021-09-20", "2pm", "Happy Day", "sonny malick", "www.cisco.com", "blah")
    print(get_all_events())
    #print(get_all_events(creator_id="blah"))
    #delete_event(5)