import mysql.connector
from mysql.connector import errorcode
import re

tables = {}
DB_NAME = 'Art'

arr_foreign_key = [
"ALTER TABLE `Paintings` ADD CONSTRAINT `Painting_fk1` FOREIGN KEY (`technics_id`) REFERENCES `Technics`(`id`);",
"ALTER TABLE `Paintings` ADD CONSTRAINT `Painting_fk2` FOREIGN KEY (`painting_styles_id`) REFERENCES `Painting styles`(`id`);",
"ALTER TABLE `Paintings` ADD CONSTRAINT `Painting_fk3` FOREIGN KEY (`periods_id`) REFERENCES `Historical periods`(`id`);",
"ALTER TABLE `Painting by artists` ADD CONSTRAINT `Painting by artists_fk0` FOREIGN KEY (`artist_id`) REFERENCES `Artists`(`id`);",
"ALTER TABLE `Painting by artists` ADD CONSTRAINT `Painting by artists_fk1` FOREIGN KEY (`paint_id`) REFERENCES `Paintings`(`id`);",
"ALTER TABLE `Tech by subtech` ADD CONSTRAINT `Tech by subtech_fk0` FOREIGN KEY (`tech_id`) REFERENCES `Technics`(`id`);",
"ALTER TABLE `Tech by subtech` ADD CONSTRAINT `Tech by subtech_fk1` FOREIGN KEY (`subtech_id`) REFERENCES `Subtechnics`(`id`);"
]

tables['Artists'] = (
'''
CREATE TABLE if not exists `Artists` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`birthday` DATE NOT NULL,
	`date_of_death` DATE NOT NULL,
	`nationality` TEXT NOT NULL,
	PRIMARY KEY (`id`)
)
''')

tables['Paintings'] = (
'''
CREATE TABLE if not exists `Paintings` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`creating_date` int NOT NULL,
	`cost_$m` float,
	`technics_id` int,
	`painting_styles_id` int,
	`periods_id` int,
	PRIMARY KEY (`id`)
)
''')

tables['Technics'] = (
'''
CREATE TABLE if not exists `Technics` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
)
''')

tables['Painting styles'] = (
'''
CREATE TABLE if not exists `Painting styles` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
)
''')

tables['Historical periods'] = (
'''
CREATE TABLE if not exists `Historical periods` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	`begin_date` int NOT NULL,
	`ending_date` int,
	PRIMARY KEY (`id`)
)
''')

tables['Painting by artists'] = (
'''
CREATE TABLE if not exists `Painting by artists` (
	`artist_id` int NOT NULL,
	`paint_id` int NOT NULL
)
''')

tables['Subtechnics'] = (
'''
CREATE TABLE `Subtechnics` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` TEXT NOT NULL,
	PRIMARY KEY (`id`)
);
''')

tables['Tech by subtech'] = (
'''
CREATE TABLE `Tech by subtech` (
	`tech_id` int NOT NULL,
	`subtech_id` int NOT NULL
);
''')

def create_database(cursor):
	try:
		cursor.execute(
			"CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
		exit(1)

def create_table(cursor) :
    print('size table :', len(tables))
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

def create_foreign_key(cursor):
    for query_create_foreign_key in  arr_foreign_key:
        try:
            print("Creating foreign_key {}: ".format(query_create_foreign_key), end='')
            cursor.execute(query_create_foreign_key)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_KEY:
                print(" already exists.")
            else:
            	print('\n',err.msg)
        else:
            print("\nOK")

def read_data_(source) :
	with open(source, 'r') as content_file:
		return content_file.read()

def init_artists(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM Artists);")
	size = cursor.fetchall()
	if  size[0][0] == 0:
		artists = read_data_('./resources/Artists.txt').splitlines()
		artists = [string.split(" ", 1)[1].split(', ') for string in artists]
		parse_date = lambda el : "-".join( (el.split("-")[::-1]) )
		values = []
		for el in artists:
			values.append( (el[0], parse_date(el[1]), parse_date(el[2]), el[3]) )

		add_artists = (""" INSERT INTO Artists
	               	    (name, birthday, date_of_death, nationality)
	                    VALUES (%s, %s, %s, %s)""")

		cursor.executemany(add_artists, values)
	else :
		print("Already added")

def init_paintings(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM Paintings);")
	size = cursor.fetchall()

	if  size[0][0] == 0:
		paintings = read_data_('./resources/Paintings.txt')
		artists_id = []
		paintings_on_id = []
		for m in re.finditer(r"(\d+) ?:(( +.+, \d+\n?)+)", paintings):
			artists_id.append(int(m.group(1)))
			paintings_on_id.append(m.group(2).split('\n '))
		paintings_on_id = [[s.strip().split(', ') for s in a] for a in paintings_on_id]
		# print( "len paintings : ", len(paintings_on_id))
		# print( "len artists : ", len(artists_id))

		v_connect = []
		inc = 1
		values = []
		for id in artists_id:
			for p_el in paintings_on_id[id-1]:
				values.append( (p_el[0], int(p_el[1]), float(p_el[2]), int(p_el[3]), int(p_el[4]), int(p_el[5])) )
				# print(id , ':' , p_el[5])
				v_connect.append((id,inc))
				inc += 1

		add_paintings = (""" INSERT INTO Paintings
	               	    (name, creating_date, cost_$m, technics_id, painting_styles_id, periods_id)
	                    VALUES (%s, %s, %s, %s, %s, %s)""")
		cursor.executemany(add_paintings, values)

		add_connection = (""" INSERT INTO `Painting by artists`
	               	    (artist_id, paint_id)
	                    VALUES (%s, %s)""")
		cursor.executemany(add_connection, v_connect)
	else :
		print("Already added")

def init_periods(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM `Historical periods`);")
	size = cursor.fetchall()

	if  size[0][0] == 0:
		data = read_data_('./resources/Historical_periods.txt')
		periods = []
		for m in re.findall(r".+, \d+, \d+\n?", data):
			periods.append(m.strip().split(', '))

		values = []
		for p in periods:
			values.append( ( p[0], int(p[1]), int(p[2]) ) )

		add_paintings = (""" INSERT INTO `Historical periods`
	               	    (name, begin_date, ending_date)
	                    VALUES (%s, %s, %s)""")

		cursor.executemany(add_paintings, values)
	else :
		print("Already added")

def init_techniques(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM Technics);")
	size = cursor.fetchall()
	if  size[0][0] == 0:
		data = read_data_('./resources/Techniques.txt')
		techniques = []
		for m in re.findall(r"\w+\n?", data):
		    techniques.append(m.strip())

		values = []
		for el in techniques:
			values.append((el, ))

		add_techniques = (""" INSERT INTO Technics
						(name)
						VALUES (%s)""")
		cursor.executemany(add_techniques, values)
	else :
		print("Already added")

def init_p_styles(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM `Painting styles`);")
	size = cursor.fetchall()
	if  size[0][0] == 0:
		data = read_data_('./resources/Painting_styles.txt')
		styles = []
		for m in re.findall(r".+\n?", data):
		    styles.append(m.strip())
		values = []
		for el in styles:
			values.append( (el, ) )

		add_styles = (""" INSERT INTO `Painting styles`
						(name)
						VALUES (%s)""")
		cursor.executemany(add_styles, values)
	else :
		print("Already added")

def init_subtechiques(cursor):
	cursor.execute("SELECT EXISTS (SELECT 1 FROM `Subtechnics`);")
	size = cursor.fetchall()
	if  size[0][0] == 0:
		subtech = read_data_('./resources/Subtechnics.txt')
		subtech_id = []
		name = []
		for m in re.finditer(r"(\d):(( +.+\n?)+)", subtech):
		    subtech_id.append(int(m.group(1)))
		    name.append(m.group(2).split('\n '))
		name = [[s.strip().split(', ') for s in a] for a in name]

		v_connect = []
		values = []
		inc = 1
		for id in subtech_id:
			for p_el in name[id-1]:
				values.append( (p_el[0], ) )
					# print(id , ':' , p_el[0])
				v_connect.append((id,inc))
				inc += 1
		# print(v_connect)
		add_subtech = (""" INSERT INTO Subtechnics
						(name)
						VALUES (%s)""")
		cursor.executemany(add_subtech, values)

		add_connection = (""" INSERT INTO `Tech by subtech`
						(tech_id, subtech_id)
						VALUES (%s, %s)""")
		cursor.executemany(add_connection, v_connect)
	else :
		print("Already added")

def initializing_db(cursor):
	init_p_styles(cursor)
	init_techniques(cursor)
	init_subtechiques(cursor)
	init_periods(cursor)
	init_artists(cursor)
	init_paintings(cursor)
