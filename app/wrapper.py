#!/usr/bin/python
###########################################################################################################
# Description:  python wrapper.py -h  --> give detailed info about arguements
# python wrapper.py -d </path/directoryname> -u <user> -H <host> -n <database name> -p <password> -P <port> 
###########################################################################################################

import sys, os
import re
import pymysql.cursors
from subprocess import PIPE, Popen
import json
import argparse
import logging


logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s: %(funcName)5s()] ====> %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class DBMigration():
    '''
    This class is used to find db version, & execute sql files from given directory location.
    '''

    def __init__(self, **kwargs):
        self.directory = kwargs['directory']
        self.dbUser = kwargs['dbUser']
        self.dbHost = kwargs['dbHost']
        self.dbName = kwargs['dbName']
        self.password = kwargs['password']
        self.port = kwargs['port']
        self.versionTable = "versionTable"
        self.connection = ""
        self.cursor = ""

    def main(self):
        self.connection = self.createDBConnection()
        self.cursor = self.connection.cursor()

        filesWithVersions = self.listSqlFilesWithVersions()
        maxFileVersion = max(list(map(lambda x:x[0],filesWithVersions)))
        dbVersion = self.fetchDBVersion()

        logger.info("Max version from sql file: {}; DB Version: {};".format(maxFileVersion, dbVersion))

        migrationFlag = False
        if int(dbVersion) < int(maxFileVersion):
            for sqlFile in filesWithVersions:
                fileVersion = sqlFile[0]
                filePath = sqlFile[1]
                if int(fileVersion) > int(dbVersion):
                    queryCmd = "mysql -h {} -P {}  --protocol=tcp -u {} -p\"{}\" -e \"SOURCE {};\" --force --verbose".format(self.dbHost, self.port, self.dbUser, self.password, filePath)
                    # logger.info("Dumping SqlFile: {}".format(queryCmd))
                    status, output, error = self.cmdSubmitter(queryCmd, True)
                    logger.info(output)
                    if status != 0:
                        raise Exception(error)
                    migrationFlag = True

        if migrationFlag:
            self.updateDBVersion(maxFileVersion)
        logger.info("versionTable updated with new DB version: {}".format(maxFileVersion))

        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return None
    

    def createDBConnection(self):
        connection = pymysql.connect(host=self.dbHost,user=self.dbUser,
                password=self.password,charset='utf8mb4',port=self.port,database=self.dbName)
                #  cursorclass=pymysql.cursors.DictCursor)
        return connection

    def listSqlFilesWithVersions(self):
        filesList = [[re.sub("\D+", "", fName), os.path.join(self.directory, fName)] \
            for fName in os.listdir(self.directory) \
            if re.match(r'^.*\.sql$', fName)]
        return sorted(filesList, key=lambda x: x[0], reverse=False)


    def fetchDBVersion(self):
        query = "SELECT * FROM {}.{};".format(self.dbName, self.versionTable)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def updateDBVersion(self, maxFileVersion):
        query = "UPDATE {}.{} SET version = \"{}\";".format(self.dbName, self.versionTable, maxFileVersion)
        self.cursor.execute(query)

    def cmdSubmitter(self,queryCmd, IsShell=None):
        logger.info('{0}'.format(str(queryCmd)))
        if IsShell:
           run_process = Popen(queryCmd, stdout=PIPE, stderr=PIPE, shell=True)
           run_output, run_error = run_process.communicate()
           return run_process.returncode, run_output, run_error

def mainParser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',help='Sql Scripts Directory Path',nargs='+',required=True)
    parser.add_argument('-u', '--dbUser',help='Database User Name',nargs='+',required=True)
    parser.add_argument('-H', '--dbHost',help='Database HostName/IP',default="localhost",nargs='+',required=False)
    parser.add_argument('-n', '--dbName',help='Database Name',nargs='+',required=True)
    parser.add_argument('-p', '--password',help='Database Password',nargs='+',required=True)
    parser.add_argument('-P', '--port',help='Database Port',nargs='+',type=int, required=True)
    args = parser.parse_args()
    args_dict = vars(args)
    logger.info(args_dict)
    #++++++++++++++++++++++++++++++++++++++++++++++++++#
    DBMigration(directory = args_dict['directory'][0],
        dbUser = args_dict['dbUser'][0],
        dbHost = args_dict['dbHost'][0] if type(args_dict['dbHost']) == list else args_dict['dbHost'],
        dbName = args_dict['dbName'][0],
        password = args_dict['password'][0],
        port = args_dict['port'][0]).main()
    #++++++++++++++++++++++++++++++++++++++++++++++++++#
    return None


if __name__ == "__main__":
    mainParser(sys.argv[1:])