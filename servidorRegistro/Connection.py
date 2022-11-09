import psycopg2
import json
from address import Address

class Connection():
  def __init__(self,credpath):
        self.conn=None
        self.credpath=credpath

  def conn_db(self):
    with open(self.credpath) as f:
      credentials=json.load(f)
    try:
      self.conn = psycopg2.connect(host=credentials['host'], 
                            database=credentials['database'],
                            user=credentials['user'], 
                            password=credentials['password'])                     
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        return False
    return True
    
  def create_db(self):
    sql = '''
    DROP TABLE IF EXISTS public.enderecos;
    CREATE TABLE public.enderecos 
      ( 
        nome  varchar(50), 
        endIP char(35), 
        porta varchar(10) 
      );'''

    succes=self.conn_db()
    if succes:
      cur = self.conn.cursor()
      try:
        cur.execute(sql)
        self.conn.commit()
      except (Exception, psycopg2.DatabaseError) as error:
          print("Error: %s" % error)
          self.conn.rollback()
          cur.close()
          self.conn.close()
          return False
      cur.close()
      self.conn.close()
      self.conn=None
      return True
    return succes

  def insert_db(self,endereco:Address):
    sql = '''
    INSERT into public.enderecos (nome,endIP,porta) 
    values('%s','%s','%s');
    '''%(endereco.nome,endereco.endIP,endereco.porta)
    self.conn_db()
    if self.conn:
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
    addr=Address(None,None,None)
    sql = '''
    select * from public.enderecos where nome='%s'
    '''%(name)
    self.conn_db()
    if self.conn:
      cur = self.conn.cursor()
      cur.execute(sql)
      result = cur.fetchall()
      if result:
        addr.nome=str(result[0][0])
        addr.endIP=str(result[0][1])
        addr.porta=str(result[0][2])
      cur.close()
      self.conn.close()
      self.conn=None
    return addr

  def read_all(self):
    adresses=[]
    sql = '''
    select * from public.enderecos
    '''
    self.conn_db()
    if self.conn:
      cur = self.conn.cursor()
      cur.execute(sql)
      result = cur.fetchall()
      if result:
        for r in result:
          addr=Address(None,None,None)
          addr.nome=r[0]
          addr.endIP=r[1]
          addr.porta=r[2]
          adresses.append(addr)
      cur.close()
      self.conn.close()
      self.conn=None
    return adresses

  def delete_by_name(self,name):
    sql = '''
    delete from public.enderecos where nome='%s'
    '''%(name)
    self.conn_db()
    if self.conn:
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

  def update_by_name(self,name,addr:Address):
    sql = '''
    update public.enderecos set nome='%s',endIP='%s',porta='%s' where nome='%s'
    '''%(addr.nome,addr.endIP,addr.porta,name)
    self.conn_db()
    if self.conn:
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