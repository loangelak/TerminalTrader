#!/usr/bin/env python3


import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
	"""INSERT INTO users(
		username,
		password,
		balance) VALUES(
		"matthewmuccio",
		"b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86",
		100000.00
	);"""
)

connection.commit()
cursor.close()
connection.close()
