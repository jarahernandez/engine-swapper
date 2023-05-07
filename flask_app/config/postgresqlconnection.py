import psycopg2
import psycopg2.extras

class PostgreSQLConnection:
    def __init__(self, db):
        conn = psycopg2.connect(host = 'localhost',
                                dbname = db,
                                user= 'postgres',
                                password = 'root',
                                port = 5432)
        self.conn = conn

    def query_db(self, query, data=None):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                query = cur.mogrify(query, data)
                print('-----> Running query:', query)
                cur.execute(query, data)
                if query.decode().lower().find("insert") >= 0:
                    self.conn.commit()
                    cur.execute("SELECT lastval()") #Get ID of last row inserted
                    last_row = cur.fetchone()
                    print('-----> Row returned by fetchone():', last_row)
                    last_row_id = last_row['lastval']
                    print('-----> Insertion successful, ID:', last_row_id)
                    return last_row_id
                elif query.decode().lower().find("select") >= 0:
                    rows = cur.fetchall()
                    results = []
                    for row in rows:
                        row_dict = {}
                        for key, value in row.items():
                            if isinstance(value, (list, tuple)):
                                row_dict[key] = list(value)
                            else:
                                row_dict[key] = value
                        results.append(row_dict)
                    print('-----> Results from fetch:', results)
                    return results
                else:
                    self.conn.commit()
            except Exception as e:
                print('-----> Something went wrong', e)
                return False
            finally:
                self.conn.close()

def connectToPostgreSQL(db):
    return PostgreSQLConnection(db)