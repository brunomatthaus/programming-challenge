import sqlite3
import csv

################################################################################
#Database creation
################################################################################

counterMax = 300000; #number of elements to add to tables per insert

try:
    conn = sqlite3.connect('sidia.db')
    print ("Database opened with success (createDBTables)")

    #Creation of table: Titles
    conn.execute('''
                CREATE TABLE TITLES(
                    TCONST TEXT PRIMARY KEY NOT NULL,
                    TITLETYPE TEXT NOT NULL,
                    PRIMARYTITLE TEXT NOT NULL,
                    ORIGINALTITLE TEXT NOT NULL,
                    ISADULT BOOLEAN NOT NULL,
                    STARTYEAR INT NOT NULL,
                    ENDYEAR INT,
                    RUNTIMEMINUTES INT
                );''')

    #Creation of table: Genres
    conn.execute('''
                CREATE TABLE GENRES(
                    TCONST TEXT,
                    GENRES TEXT,
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')

    #Creation of table: Ratings
    conn.execute('''
                CREATE TABLE RATINGS(
                    TCONST TEXT,
                    NUMVOTES INT NOT NULL,
                    AVERAGERATING REAL NOT NULL,
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')

    #Creation of table: Names
    conn.execute('''
                CREATE TABLE NAMES(
                    NCONST TEXT NOT NULL,
                    PRIMARYNAME TEXT NOT NULL,
                    BIRTHYEAR INT,
                    DEATHYEAR INT
                );''')

    #Creation of table: knownForTitles
    conn.execute('''
                CREATE TABLE KNOWNFORTITLES(
                    NCONST TEXT,
                    TCONST TEXT,
                    FOREIGN KEY(NCONST) REFERENCES NAMES(NCONST),
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')

    #Creation of table: Professions
    conn.execute('''
                CREATE TABLE PROFESSIONS(
                    NCONST TEXT,
                    PRIMARYPROFESSION TEXT NOT NULL,
                    FOREIGN KEY(NCONST) REFERENCES NAMES(NCONST)
                );''')

    conn.close()

    print("Database [sidia.db] created with success!")

except sqlite3.Error as error:
    print("Connection error at: createDBTables - ", error)


################################################################################
#Inserting data in the database
################################################################################

#inserting Title data
try:
    conn = sqlite3.connect('sidia.db')
    with open("dataTitle.tsv", encoding='utf-8') as titleData:

        cursor = conn.cursor()
        next(titleData) #Skip first line
        tsvreader = csv.reader(titleData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #Counter to insert data at counterMax elements

        dadosT = [] #Title data list to be inserted in the database at counterMax elements
        dadosG = [] #Genre data list to be inserted in the database at counterMax elements

        for line in tsvreader:

            cont = cont + 1
            for i in range(5,9): #setting all empty or "\N" values to "null"

                if((line[i] == "\\N") or (len(line[i])) == 0):
                    line[i] = "null";

            dadoT = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]);
            dadosT.append(dadoT) #add all data up until line[7]

            dadoG = (line[8].split(",")) #split on column 9 (title genres)
            for i in dadoG:
                    dadosG.append([line[0],i]) #Genre data list of each title

            if(cont == counterMax): #at counterMax elements -> insert in the database with executemany -> clear all lists and reset counter
                cont = 0

                cursor.executemany("INSERT INTO TITLES(TCONST,TITLETYPE,PRIMARYTITLE,ORIGINALTITLE,ISADULT,STARTYEAR,ENDYEAR,RUNTIMEMINUTES) VALUES (?,?,?,?,?,?,?,?);",(dadosT))
                conn.commit()
                dadosT = []
                cursor.executemany("INSERT INTO GENRES(TCONST,GENRES) VALUES (?,?);",(dadosG))
                conn.commit()
                dadosG = []

        #insert the leftover data in the lists
        if(dadosT):
            cursor.executemany("INSERT INTO TITLES(TCONST,TITLETYPE,PRIMARYTITLE,ORIGINALTITLE,ISADULT,STARTYEAR,ENDYEAR,RUNTIMEMINUTES) VALUES (?,?,?,?,?,?,?,?);",(dadosT))
            conn.commit()

        if(dadosG):
            cursor.executemany("INSERT INTO GENRES(TCONST,GENRES) VALUES (?,?);",(dadosG))
            conn.commit()

    conn.close()

except sqlite3.Error as error:
    print("Connection error at: dataTitle.tsv ", error, line)


#inserting Ratings data
try:
    conn = sqlite3.connect('sidia.db')
    with open("dataRatings.tsv", encoding='utf-8') as ratingsData:

        cursor = conn.cursor()
        next(ratingsData) #skip first line
        tsvreader = csv.reader(ratingsData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #Counter to insert data at counterMax elements

        dadosR = [] #Ratings data list to be inserted in the database at counterMax elements

        for line in tsvreader:

            cont = cont + 1

            dadoR = (line[0],line[1],line[2])
            dadosR.append(dadoR) #add all data in this line to the list

            if(cont == counterMax): #at counterMax elements -> insert in the database with executemany -> clear all lists and reset counter
                cont = 0

                cursor.executemany("INSERT INTO RATINGS(TCONST,AVERAGERATING,NUMVOTES) VALUES (?,?,?);",(dadosR))
                conn.commit()
                dadosR = []

        #insert the leftover data in the lists
        if(dadosR):
            cursor.executemany("INSERT INTO RATINGS(TCONST,AVERAGERATING,NUMVOTES) VALUES (?,?,?);",(dadosR))
            conn.commit()

    conn.close()

except sqlite3.Error as error:
    print("Connection error at: dataRatings.tsv ", error)


#inserting Names data
try:
    conn = sqlite3.connect('sidia.db')
    with open("dataName.tsv", encoding='utf-8') as nameData:

        cursor = conn.cursor()
        next(nameData) #skip first line
        tsvreader = csv.reader(nameData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #Counter to insert data at counterMax elements

        dadosN = [] #Names data list to be inserted in the database at counterMax elements
        dadosK = [] #knownForTitles data list to be inserted in the database at counterMax elements
        dadosP = [] #Professions data list to be inserted in the database at counterMax elements

        for line in tsvreader:

            cont = cont + 1

            for i in range(1,6): #setting all empty or "\N" values to "null"
                if((line[i] == "\\N") or (len(line[i])) == 0):
                    line[i] = "null";

            dadoN = (line[0],line[1],line[2],line[3])
            dadosN.append(dadoN) #insert line data up until line[3]

            dadoP = (line[4].split(",")) #split on column 5 (professions)
            for i in dadoP:
                dadosP.append([line[0],i]) #add nconst and professions to the list

            dadoK = (line[5].split(",")) #split on column 6 (knownForTitles)
            for i in dadoK:
                dadosK.append([line[0],i]) #add nconst and tconst to the list

            if(cont == counterMax): #at counterMax elements -> insert in the database with executemany -> clear all lists and reset counter
                cont = 0

                cursor.executemany("INSERT INTO NAMES(NCONST,PRIMARYNAME,BIRTHYEAR,DEATHYEAR) VALUES (?,?,?,?);",(dadosN))
                conn.commit()
                dadosN = []

                cursor.executemany("INSERT INTO PROFESSIONS(NCONST,PRIMARYPROFESSION) VALUES (?,?);",(dadosP))
                conn.commit()
                dadosP = []

                cursor.executemany("INSERT INTO KNOWNFORTITLES(NCONST,TCONST) VALUES (?,?);",(dadosK))
                conn.commit()
                dadosK = []

        #insert the leftover data in the lists
        if(dadosN):
            cursor.executemany("INSERT INTO NAMES(NCONST,PRIMARYNAME,BIRTHYEAR,DEATHYEAR) VALUES (?,?,?,?);",(dadosN))
            conn.commit()

        if(dadosP):
            cursor.executemany("INSERT INTO PROFESSIONS(NCONST,PRIMARYPROFESSION) VALUES (?,?);",(dadosP))
            conn.commit()

        if(dadosK):
            cursor.executemany("INSERT INTO KNOWNFORTITLES(NCONST,TCONST) VALUES (?,?);",(dadosK))
            conn.commit()

    conn.close()
    print("Finished inserting data.")
except sqlite3.Error as error:
    print("Connection error at: dataName.tsv ", error)
