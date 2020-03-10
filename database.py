import time
import mysql.connector
from mysql.connector import errorcode

class Database:
    def __init__(self, user, password):
        self.password = password
        self.user = user
        self.cmd = None
        try:
            self.cmd = mysql.connector.connect(
                host='192.168.1.34',
                user=self.user,
                password=self.password
            )
        except mysql.connector.Error as err :
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR :
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR :
                print("Database does not exist")
            else :
                print(err)
        else :
            print('connected')
    def createDB(self,dbname):
        try:
            self.cmd.cursor().execute('CREATE DATABASE {}'.format(dbname))
            print('DB: {}, criado com sucesso'.format(dbname))
        except Exception as e:
            if errorcode.ER_DB_CREATE_EXISTS:
                print('Tabela: {}, ja existe(:'.format(dbname))
            else:
                print('erro ao criar a DB {}'.format(dbname))
                print('error name {}'.format(e))
    def deleteDB(self,dbname):
        try:
            self.cmd.cursor().execute('DROP DATABASE {}'.format(dbname))
            print('DB: {}, deleted with sucess '.format(dbname))
        except Exception as e:
            print('erro ao deletar a DB {}'.format(dbname))
            print('error name {}'.format(e))
    def createTable(self, dbname,tableName, *args):
        try:
            qry = ''
            b = 1
            a = len(args)
            for i in args:
                qry+=i
                if a != b:
                    qry+=','
                b+=1
            self.cmd.cursor().execute('USE {}'.format(dbname))
            #print('CREATE TABLE {}({})'.format(tableName,qry))
            self.cmd.cursor().execute('CREATE TABLE {}({})'.format(tableName,qry))
            print('Tabela: {}, criado com sucesso'.format(tableName))
        except Exception as e :
            if errorcode.ER_TABLE_EXISTS_ERROR:
                print('Tabela: {}, ja existe(:'.format(tableName))
            else:
                print('erro ao criar a tabela {}'.format(tableName))
                print('error name {}'.format(e))
    def __del__(self):
        self.cmd.close()
    def setup(self):
        #self.createDB('myPosts')
        #self.createTable('myPosts', 'post_1', 'id_user_liked VARCHAR(20)', 'id_user_comment VARCHAR(20)')

        #self.createDB('hashtag')
        #self.createTable('myPosts', 'post_1', 'id_user_liked VARCHAR(20)', 'id_user_comment VARCHAR(20)')

        self.createDB('user')
        self.createTable('user','user_info',
            'id_user VARCHAR(20)',
            'qtdLIKEHASH INT',
            'qtdLIKEMYPOSTS INT',
            'followME BOOLEAN',
            'ACCURACY FLOAT'
        )
    def insert(self, dbname, tablename, values):
        try:
            self.cmd.cursor().execute('USE {}'.format(dbname))
            self.cmd.cursor().execute('INSERT INTO {} ({}) VALUES({});'.format(tablename,self.getColumn(dbname,tablename),values))
            self.cmd.commit()
            print('insert feito com sucesso db: {}'.format(dbname))

        except Exception as e :
            print('erro ao ao insertar a DB {}'.format(tablename))
            print('error name {}'.format(e))
    def deleteTable(self, dbname, tablename):
        try:
            self.cmd.cursor().execute('USE {}'.format(dbname))
            self.cmd.cursor().execute('DROP TABLE {}'.format(tablename))
            print('tabela {} deletada com sucesso'.format(tablename))


        except Exception as e :
            print('erro ao ao deletar a tabela {}'.format(tablename))
            print('error name {}'.format(e))
    def updateTable(self, dbname, tablename, columnName, value, user):
        try:
            self.cmd.cursor().execute('USE {}'.format(dbname))
            self.cmd.cursor().execute('UPDATE {} SET {}={} WHERE id_user={}'.format(tablename, columnName, value, user))
            self.cmd.commit()
            print('tabela {} atualizada com sucesso'.format(tablename))

        except Exception as e :
            print('erro ao atualizar a tabela {}'.format(tablename))
            print('error name {}'.format(e))
    def read(self,dbname,username,tablename, fieldName):
        try:
            a = self.cmd.cursor()
            a.execute('USE {}'.format(dbname))
            a.execute('SELECT * FROM  {} WHERE {}={};'.format(tablename,fieldName,username))
            output = a.fetchall()
            return output
        except Exception as e:
            print(e)
    def getColumn(self, dbname, tableName):
        try:
            query = ''
            c = 1
            a = self.cmd.cursor()
            a.execute('USE {}'.format(dbname))
            a.execute('DESCRIBE {}'.format(tableName))
            output = a.fetchall()
            l = len(output)
            for i in output:
                query += i[0]
                if c != l:
                    query+=','
                    c+=1
            return query
        except Exception as e:
            print(e)
    def count(self,dbname,tablename):
        try:
            a = self.cmd.cursor()
            a.execute('USE {}'.format(dbname))
            a.execute('SELECT COUNT(*) FROM {}'.format(tablename))
            output = a.fetchall()
            c = output[0][0]
            print('a Tabela {} tem {} resultados'.format(tablename, c))
            return c
        except Exception as e:
            print('erro ao contar a tabela {}', format(tablename))
            print(e)
            return 99

#db = Database('homePC', 'iagomlkzika1')