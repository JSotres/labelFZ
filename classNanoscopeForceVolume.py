###############################################################################
# Imports
###############################################################################
import re
import numpy as np
import argparse
import sqlite3
import io
import matplotlib.pyplot as plt

###############################################################################
# numpy arrays are not supported by sqlite. We need to register them as new
# data types. For this, we need to create an adapter and a converter.
###############################################################################


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

###############################################################################
# A class named NanoscopeForceVolumeObject is declared, which contains
# all neccesary methods for reading data from force volume files and storing
# it in a sqlite database
###############################################################################


class NanoscopeForceVolumeObject():
    '''
    Class to handle Force Volume Files.
    It allows reading Nanoscope 9 Force Volume Files and save
    the raw and metadata to a SQLite database.
    It also allows accesing the database by means of dedicated functions.

    Attributes:
        connector to the database
        cursor to the database

    Methods:
        __init__(): 
            no attributes are created, but it is here where the adapter
            and converter needed for sqlite to handle numpy arrays are called.
        fvToSQL(file_name, database_name):
            reads metadata and raw data from file_name and stores it in the
            data base database_name
        readHeader(file_name):
        headerToParameters(headerParameters):
        readTopography(file_name, headerParameters, fvParameters):
        readFV(file_name, headerParameters, fvParameters):
        connectToDataBase(database_name)
        closeDataBaseConnection()
        createTables(file_name2)
        populateTables(file_name2, fvParameters, topographyArray, fvDataArray)
        getForwardForceRampFromID(database_name, idx, xDimensions=True)
        getNumberForceRamps(database_name)
        
    Database: For a force volume file, fvToSQL creates 2 tables:
        
        ExperimentalParametersTable. Columns:
            id INTEGER
            ExperimentName TEXT NOT NULL UNIQUE
            nRows INTEGER
            nColumns INTEGER,
            nRampPoints INTEGER
            scanSize REAL
            rampLength REAL
            photodiodeSensitivity REAL DEFAULT 1
            forceConstant REAL DEFAULT 1
            probeRadius REAL DEFAULT 1

        RawDataTable. Columns:
            id INTEGER,
            ExperimentID INTEGER NOT NULL,
            NX INTEGER,
            NY INTEGER,
            ForceForward array,
            ForceBackward array,
            Height REAL,
            PRIMARY KEY (id),
            FOREIGN KEY (ExperimentID) REFERENCES ExperimentalParametersTable(id)
    '''

    def __init__(self):
        '''
        Initializes an object of the class NanoscopeForceVolumeObject.
        It is here also where the adapter and converter for
        sqlite3 numpy array to bytes conversions are registered.
        uses it for reading the data in the parsed Force Volume file
        and saves it in a sqlite database.
        '''

        # Register adapter and converter for
        # sqlite3 numpy array to bytes conversions
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)

        

    def fvToSQL(self, file_name, database_name):
        '''
        Method that handles the reading of the force volume 
        file file_name, and saves the raw and metadata in the
        sqlite database database_name
        '''

        # Name of the Force Volume file to be used in the database
        # SQLite does not like dots...
        file_name2 = file_name.replace('.', '_')

        headerParameters = self.readHeader(file_name)

        fvParameters = self.headerToParameters(headerParameters)

        topographyArray = self.readTopography(file_name, headerParameters, fvParameters)

        fvDataArray = self.readFV(file_name, headerParameters, fvParameters)

        self.connectToDataBase(database_name)

        self.createTables(file_name2)

        self.populateTables(file_name2, fvParameters, topographyArray, fvDataArray)

        self.closeDataBaseConnection()

    def getForwardForceRampFromID(self, database_name, idx, direction='ForceForward', xDimensions=True):

        self.connectToDataBase(database_name)

        sql_command0 = f"""
                      SELECT {direction}
                      FROM RawDataTable
                      WHERE id = {idx};
                      """
        self.cursor.execute(sql_command0)

        data = self.cursor.fetchone()
        
        yData = data[0]

        sql_command1 = f"""
                      SELECT rampLength, nRampPoints
                      FROM ExperimentalParametersTable
                      WHERE id = 1;
                      """
        self.cursor.execute(sql_command1)
        data = self.cursor.fetchone()
        
        if xDimensions == True:
            xData = np.linspace(0., data[0], data[1])
        else:
            xData = np.linspace(0, data[1]-1, data[1])
            
        return(xData, yData)

        self.closeDataBaseConnection()

    def getNumberForceRamps(self, database_name):

        self.connectToDataBase(database_name)

        sql_command1 = f"""
                      SELECT nRows, nColumns
                      FROM ExperimentalParametersTable
                      WHERE id = 1;
                      """
        self.cursor.execute(sql_command1)
        data = self.cursor.fetchone()
        
        nForceRamps = data[0] * data[1]

        return nForceRamps
        
        self.closeDataBaseConnection()

    def readHeader(self, file_name):
        '''
        Reads the header of the Force Volume File file_name
        '''
        file = open(file_name, 'r', encoding='cp1252')

        # At the beginning we are not at the end of the header
        # or at the endof the file
        header_end = 0
        eof = 0

        # We initialize the attribute headerParameters, a dictionary
        # with keys corresponding to strings that identify the lines
        # in the Force Volume file header with relevant information
        headerParameters = {'Sens. Zsens': [], '2:Z scale': [],
                            'Samps/line': [], 'Data offset': [],
                            'Scan Size': [], 'Z magnify': [],
                            '4:Ramp Size': [], 'Force Data Points': [],
                            'Number of lines': [], 'Data length':[],
                            'Bytes/pixel':[], 'Image Data':[]}

        # Keep reading the file line by line until the end of
        # the header (or the end of the file) is reached.
        # For each line, check whether it contains the keys
        # of headParameters, and if so populate their values, by
        # calling to searchForParameters(). Then, check if the end
        # of the header has been reached by calling searchForHeaderEnd()
        while (not header_end) and (not eof):
            for line in file:
                headerParameters = self.searchForParameters(line, headerParameters)
                header_end = self.searchForHeaderEnd(line, r'\*File list end')
                if header_end == 1:
                    break
            else:
                eof = 1
        file.close()

        return headerParameters

    def searchForParameters(self, _line, headerParameters):
        '''
        Identifies whether the input string, _line, contains one of the
        keys of headParameters. If so, pupulates its values with numbers
        contained in _line as well.
        '''
        for key in headerParameters:
            if re.search(re.escape(key), _line):
                if key == "Image Data":
                    searchString = re.split(r'"', _line)
                    searchString = searchString[-2]
                    headerParameters[key].append(searchString)
                else:
                    numbers = re.findall(r'\d+\.?\d*', _line)
                    # If _line contains the strings 'LSB' or '@', only populate
                    # the key value with the last number from _line. If not,
                    # populate it with all numbers.
                    if re.search(r'LSB', _line) or re.search(r'@', _line):
                        headerParameters[key].append(float(numbers[-1]))
                    else:
                        for number in numbers:
                            headerParameters[key].append(float(number))
        return headerParameters

    def searchForHeaderEnd(self, _line, _string):
        '''
        Checks if the end of the header has been reached
        '''
        if re.search(r'\*File list end', _line):
            header_end = 1
        else:
            header_end = 0

        return header_end

    def headerToParameters(self, headerParameters):
        '''
        Obtains meaningful, understandable, parameters from the key values
        from headParameters.
        '''
        fvParameters = {'numberOfMapRows':[], 'numberOfMapColumns':[],
                        'scanSize':[], 'rampLength':[],
                        'rampPoints':[], 'rampStep':[],
                        'pixelLengthColumn':[], 'pixelLengthRow':[]}
        
        fvParameters['numberOfMapRows'].append(int(headerParameters['Number of lines'][0]))
        fvParameters['numberOfMapColumns'].append(int(headerParameters['Samps/line'][0]))
        fvParameters['scanSize'].append(float(headerParameters['Scan Size'][0]))
        fvParameters['rampLength'].append(float(headerParameters['4:Ramp Size'][0] * headerParameters['Sens. Zsens'][0]))
        fvParameters['rampPoints'].append(int(headerParameters['Samps/line'][1]))
        fvParameters['rampStep'].append(fvParameters['rampLength'][0]/(fvParameters['rampPoints'][0]-1))
        fvParameters['pixelLengthColumn'].append(fvParameters['scanSize'][0]/fvParameters['numberOfMapColumns'][0])
        fvParameters['pixelLengthRow'].append(fvParameters['scanSize'][0]/fvParameters['numberOfMapRows'][0])

        return fvParameters

    def readTopography(self, file_name, headerParameters, fvParameters):
        '''
        Reads (binary) topography data contained in the Force Volume file
        and (temporally) saves it in the attribute topographyArray
        '''

        # Get index for the Data offset and Data length corresponding to the
        # topography map
        index = next(
            idx for idx in reversed(range(len(headerParameters['Image Data']))) if headerParameters['Image Data'][idx] == 'Height')
        file = open(file_name, 'rb')
        file.seek(int(headerParameters['Data offset'][index-1]))
        s = file.read(int(headerParameters['Data length'][index]))
        topographyArray = np.frombuffer(s, dtype='int32').reshape(
                (fvParameters['numberOfMapRows'][0], fvParameters['numberOfMapColumns'][0])
        )
        topographyArray = topographyArray * (
                (headerParameters['Sens. Zsens'][0] *
                 headerParameters['2:Z scale'][0]) /
                (65535+1)
        )
        file.close()

        return topographyArray

    def readFV(self, file_name, headerParameters, fvParameters):
        '''
        Reads (binary) force volume data contained in the Force Volume file
        and (temporally) saves it in the attribute FVDataArray
        '''
        # Get index for the Data offset and Data length corresponding to the
        # force volume data
        index = next(
            idx for idx in reversed(range(len(headerParameters['Image Data']))) if headerParameters['Image Data'][idx] == 'Deflection Error')
        file = open(file_name, 'rb')
        file.seek(int(headerParameters['Data offset'][index-1]))
        bufferedData = file.read(int(headerParameters['Data length'][index]))
        fvDataArray = np.frombuffer(
                bufferedData, dtype='int32', count=-1
        ).reshape(
                (fvParameters['numberOfMapRows'][0],
                 fvParameters['numberOfMapColumns'][0],
                 2,
                 fvParameters['rampPoints'][0])
        )*0.000375
        file.close()

        return fvDataArray

    def connectToDataBase(self, database_name):
        '''
        Connects to the database
        '''
        self.connector = sqlite3.connect(
                database_name,
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.cursor = self.connector.cursor()

    def closeDataBaseConnection(self):
        '''
        Closes the connection to the database
        '''
        self.cursor.close()
        self.connector.close()

    def createTables(self, file_name2):
        '''
        Creates 2 tables in the database.
        1- ExperimentsTable: a row for each force volume experiment
        with columns associated with experimental parameters of relevance.
        It is created only if it does not exists already.
        2- A table named as the input file with columns for the Force
        Volume and topography data of the specific loaded experiment. If
        a table with the same name existed, the old one is previously
        deleted.
        '''

        sql_command0 = """
        DROP TABLE IF EXISTS ExperimentalParametersTable
        """

        sql_command1 = """
        CREATE TABLE IF NOT EXISTS ExperimentalParametersTable (
        id INTEGER,
        ExperimentName TEXT NOT NULL UNIQUE,
        nRows INTEGER,
        nColumns INTEGER,
        nRampPoints INTEGER,
        scanSize REAL,
        rampLength REAL,
        photodiodeSensitivity REAL DEFAULT 1,
        forceConstant REAL DEFAULT 1,
        probeRadius REAL DEFAULT 1,
        PRIMARY KEY (id)
        );
        """
        sql_command2 = f"""
        DROP TABLE IF EXISTS RawDataTable
        """
        sql_command3 = f"""
        CREATE TABLE IF NOT EXISTS RawDataTable (
        id INTEGER,
        ExperimentID INTEGER NOT NULL,
        NX INTEGER,
        NY INTEGER,
        ForceForward array,
        ForceBackward array,
        Height REAL,
        PRIMARY KEY (id),
        FOREIGN KEY (ExperimentID) REFERENCES ExperimentalParametersTable(id)
        );
        """
        self.cursor.execute(sql_command0)
        self.cursor.execute(sql_command1)
        self.cursor.execute(sql_command2)
        self.cursor.execute(sql_command3)
        self.connector.commit()

    def populateTables(self, file_name2, fvParameters, topographyArray, fvDataArray):
        '''
        Populates the tables ExperimentalParametersTable and the one named as
        the input file.
        If an entry with a similar ExperimentName already exists in
        ExperimentsTable, thant entry is replaced.
        '''
        sql_command = """
        INSERT OR REPLACE INTO ExperimentalParametersTable
        (ExperimentName, nRows, nColumns,
        nRampPoints, scanSize, rampLength) values
        (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql_command, (
            file_name2,
            fvParameters['numberOfMapRows'][0],
            fvParameters['numberOfMapColumns'][0],
            fvParameters['rampPoints'][0],
            fvParameters['scanSize'][0],
            fvParameters['rampLength'][0]
        ))

        sql_command2 = f"""
        SELECT id FROM ExperimentalParametersTable
        WHERE ExperimentName='{file_name2}';
        """
        self.cursor.execute(sql_command2)

        ExperimentID = self.cursor.fetchone()[0]

        for i in range(fvParameters['numberOfMapRows'][0]):
            for j in range(fvParameters['numberOfMapColumns'][0]):
                self.cursor.execute(
                        f"""INSERT INTO RawDataTable
                           (ExperimentID, NX, NY,
                           ForceForward, ForceBackward, Height)
                           values (?, ?, ?, ?, ?, ?)""",
                        (ExperimentID, i, j, fvDataArray[i, j, 0, :],
                         fvDataArray[i, j, 1, :],
                         topographyArray[i, j])
                        )
        self.connector.commit()

    


###############################################################################
# Run if this is the main program
###############################################################################
if __name__ == "__main__":
    # Load parsed input force volume file and output database
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
                    help="path to input force volume file")
    ap.add_argument("-o", "--output", required=True,
                    help="path to output database")
    args = vars(ap.parse_args())

    # Register adapter and converter for
    # sqlite3 numpy array to bytes conversions
    #sqlite3.register_adapter(np.ndarray, adapt_array)
    #sqlite3.register_converter("array", convert_array)

    # Create an object of the NanoscopeForceVolumeFileToDataBase class
    fvObject = NanoscopeForceVolumeObject()

    file_name3 = args['input'].replace('.', '_')

    fvObject.fvToSQL(args['input'], args['output'])

    #fvObject.test1(args['output'])

    fvObject.getForceRampFromID(args['output'], 20)
    fvObject.getForceRampFromID(args['output'], 30)

    fvObject.getNumberForceRamps(args['output'])

    
