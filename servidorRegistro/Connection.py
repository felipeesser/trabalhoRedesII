import psycopg2
import json
from endereco import Endereco

class Connection():
  def __init__(self,credpath):
        self.conn=None
        self.credpath=credpath

  def conn_db(self):
    with open(self.credpath) as f:
      credentials=json.load(f)
    self.conn = psycopg2.connect(host=credentials['host'], 
                          database=credentials['database'],
                          user=credentials['user'], 
                          password=credentials['password'])
    
  def create_db(self):
    sql = '''
    DROP TABLE IF EXISTS public.enderecos;
    CREATE TABLE public.enderecos 
      ( 
        nome  varchar(50), 
        endIP char(35), 
        porta varchar(10) 
      );'''
    self.conn_db()
    cur = self.conn.cursor()
    cur.execute(sql)
    self.conn.commit()
    cur.close()
    self.conn.close()
    self.conn=None

  def insert_db(self,endereco:Endereco):
    sql = '''
    INSERT into public.enderecos (nome,endIP,porta) 
    values('%s','%s','%s');
    '''%(endereco.nome,endereco.endIP,endereco.porta)
    self.conn_db()
    cur=self.conn.cursor()
    try:
        cur.execute(sql)
        self.conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        self.conn.rollback()
        cur.close()
        self.conn.close()
        return
    cur.close()
    self.conn.close()
    self.conn=None

  def read_by_name(self,name):
    sql = '''
    select * from public.enderecos where nome='%s'
    '''%(name)
    self.conn_db()
    cur = self.conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    e=Endereco(None,None,None)
    if result:
      e.nome=result[0][0]
      e.endIP=result[0][1]
      e.porta=result[0][2]
    cur.close()
    self.conn.close()
    self.conn=None
    return e

  def delete_by_name(self,name):
    sql = '''
    delete from public.enderecos where nome='%s'
    '''%(name)
    self.conn_db()
    cur = self.conn.cursor()
    try:
        cur.execute(sql)
        self.conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        self.conn.rollback()
        cur.close()
        self.conn.close()
        return
    self.conn.close()
    self.conn=None

  def update_by_name(self,name,e):
    sql = '''
    update public.enderecos set nome='%s',endIP='%s',porta='%s' where nome='%s'
    '''%(e.nome,e.endIP,e.porta,name)
    self.conn_db()
    cur = self.conn.cursor()
    try:
        cur.execute(sql)
        self.conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        self.conn.rollback()
        cur.close()
        self.conn.close()
        return
    self.conn.close()
    self.conn=None

def main():
  #create
   c=Connection('credentials.json')
   c.conn_db()
   c.create_db()
  #insert
   e=Endereco('teste','11111111.11111111.11111111.11111111','5000')
   c.insert_db(e)
   e=c.read_by_name('teste')
   e.tostring()
  #update 
   e=Endereco('update','0000000.11111111.11111111.11111111','4000')
   c.update_by_name('teste',e)
   e=c.read_by_name('update')
   e.tostring()
  #delete
   c.delete_by_name('teste')
   e=c.read_by_name('teste')
   e.tostring()
   
if __name__ == '__main__':
    main()