import unittest
from address import Address
from Connection import Connection

class TestCrud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=Connection('credentials.json')
        cls.a1=Address('teste1','11111111.11111111.11111111.11111111','5000')
        cls.a2=Address('teste2','11111111.11111111.11111111.00000000','4500')
    
    @classmethod
    def tearDownClass(cls):
        cls.c.create_db()

    def test_create(self):
        result=self.c.create_db()
        self.assertEqual(result,True)

    def test_insert_read(self):
        self.c.create_db()
        
        self.c.insert_db(self.a1)
        self.a1=self.c.read_by_name('teste1')
        self.assertEqual(self.a1.nome,'teste1')
        self.assertEqual(self.a1.endIP,'11111111.11111111.11111111.11111111')
        self.assertEqual(self.a1.porta,'5000')
    
    def test_read_all(self):
        self.c.create_db()
        
        self.c.insert_db(self.a1)
        self.c.insert_db(self.a2)
        result=self.c.read_all()

        self.assertEqual(len(result),2)

    def test_update(self):
        self.c.create_db()
        
        self.c.insert_db(self.a1)
        self.a1=self.c.read_by_name('teste1')
        self.assertEqual(self.a1.nome,'teste1')
        self.assertEqual(self.a1.endIP,'11111111.11111111.11111111.11111111')
        self.assertEqual(self.a1.porta,'5000')

        self.c.update_by_name('teste1',self.a2)
        a3=self.c.read_by_name('teste2')
        self.assertEqual(a3.nome,'teste2')
        self.assertEqual(a3.endIP,'11111111.11111111.11111111.00000000')
        self.assertEqual(a3.porta,'4500')

    def test_delete(self):
        self.c.create_db()
        
        self.c.insert_db(self.a1)
        self.a1=self.c.read_by_name('teste1')
        self.assertEqual(self.a1.nome,'teste1')
        self.assertEqual(self.a1.endIP,'11111111.11111111.11111111.11111111')
        self.assertEqual(self.a1.porta,'5000')

        self.c.delete_by_name('teste1')
        self.a1=self.c.read_by_name('teste1')
        self.assertEqual(self.a1.nome,None)
        self.assertEqual(self.a1.endIP,None)
        self.assertEqual(self.a1.porta,None)

if __name__ == '__main__':
    unittest.main()