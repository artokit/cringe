import psycopg2 as pg

connect = pg.connect(host='localhost', port=5431, user='admin', password='admin', database='production')
cursor = connect.cursor()
