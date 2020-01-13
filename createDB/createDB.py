import sqlite3
import csv

################################################################################
#inicio da criacao do bd
################################################################################

try:
    conn = sqlite3.connect('sidia.db')
    print ("DB aberto com sucesso (createDBTables)")


    #criacao da tabela Titles
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
    print ("Tabela Titles criada com sucesso")

    #criacao da tabela Genres
    conn.execute('''
                CREATE TABLE GENRES(
                    TCONST TEXT,
                    GENRES TEXT,
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')
    print ("Tabela Genres criada com sucesso")

    #criacao da tabela Ratings
    conn.execute('''
                CREATE TABLE RATINGS(
                    TCONST TEXT,
                    NUMVOTES INT NOT NULL,
                    AVERAGERATING REAL NOT NULL,
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')
    print ("Tabela Ratings criada com sucesso")

    #criacao da tabela Names
    conn.execute('''
                CREATE TABLE NAMES(
                    NCONST TEXT NOT NULL,
                    PRIMARYNAME TEXT NOT NULL,
                    BIRTHYEAR INT NOT NULL,
                    DEATHYEAR INT
                );''')
    print ("Tabela Names criada com sucesso")

    #criacao da tabela knownForTitles
    conn.execute('''
                CREATE TABLE KNOWNFORTITLES(
                    NCONST TEXT,
                    TCONST TEXT,
                    FOREIGN KEY(NCONST) REFERENCES NAMES(NCONST),
                    FOREIGN KEY(TCONST) REFERENCES TITLES(TCONST)
                );''')
    print ("Tabela knownForTitles criada com sucesso")

    #criacao da tabela Professions
    conn.execute('''
                CREATE TABLE PROFESSIONS(
                    NCONST TEXT,
                    PRIMARYPROFESSION TEXT NOT NULL,
                    FOREIGN KEY(NCONST) REFERENCES NAMES(NCONST)
                );''')
    print ("Tabela Professions criada com sucesso")

    conn.close()

    print("Banco de dados [sidia.db] criado com sucesso!")

except sqlite3.Error as error:
    print("Erro de conexao (createDBTables)", error)

################################################################################
#fim da criacao do bd
################################################################################
#inicio da insercao de dados no bd
################################################################################

#inserindo dados do arquivo tsv de Titles
try:
    conn = sqlite3.connect('sidia.db')
    print ("Opened database successfully (inserir Titles)")
    with open("dataTitle.tsv") as titleData:

        print("dataTitle.tsv aberto com sucesso! Iniciando insercao de dados no bd...")
        x = 0 #apagar isso
        cursor = conn.cursor()
        next(titleData) #Pula primeira linha
        tsvreader = csv.reader(titleData, delimiter="\t")
        print("0%")

        for line in tsvreader:

            for i in range(5,9):
                if(line[i] == "\\N"):
                    line[i] = "null";

            cursor.execute('''
                            INSERT INTO TITLES(TCONST,TITLETYPE,PRIMARYTITLE,ORIGINALTITLE,ISADULT,STARTYEAR,ENDYEAR,RUNTIMEMINUTES) VALUES (?,?,?,?,?,?,?,?);
                           ''',(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]))
            conn.commit()


            genresList = line[8].split(",")
            for i in genresList:
                cursor.execute('''
                                INSERT INTO GENRES(TCONST,GENRES) VALUES (?,?);
                               ''',(line[0],i))
                conn.commit()



            if(line[0] == "tt0239164"):
                print("20%")
            if(line[0] == "tt0773975"):
                print("40%")
            if(line[0] == "tt2075277"):
                print("60%")
            if(line[0] == "tt6135712"):
                print("80%")
            if(line[0] == "tt9916778"):
                print("100%")

            x = x + 1
            if (x>5):
                break
    conn.close()

except sqlite3.Error as error:
    print("Erro de conexao inserindo dataTitle.tsv", error)
