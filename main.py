import sqlite3

connection=sqlite3.connect("pm_chat.db")
cursor=connection.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS `PMC` (
            `username` VARCHAR(18) NOT NULL,
            `email` VARCHAR(250) NULL,
            `password` VARCHAR(32) NOT NULL,
            `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (`username`),
            UNIQUE (`email`)
        )
    ''')

print("PMC has been created")

connection.close()



