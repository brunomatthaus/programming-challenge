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
                    BIRTHYEAR INT,
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
    print ("DB acessado com sucesso. (inserir Titles)")
    with open("dataTitle.tsv", encoding='utf-8') as titleData:

        print("dataTitle.tsv aberto com sucesso! Iniciando insercao de dados no bd...")
        cursor = conn.cursor()
        next(titleData) #Pula primeira linha
        tsvreader = csv.reader(titleData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #contador para insercao de dados no banco a cada 100.000 elementos

        dadosT = [] #lista de dados de titles para serem inseridos no bd ao completar 100.000 elementos
        dadosG = [] #lista de dados de genres para serem inseridos no bd ao completar 100.000 elementos

        for line in tsvreader:

            cont = cont + 1
            for i in range(5,9): #onde tiver \N ou "vazio" será salvo como null

                if((line[i] == "\\N") or (len(line[i])) == 0):
                    line[i] = "null";

            dadoT = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7]);
            dadosT.append(dadoT) #adiciona linha na lista até a coluna 8 para quando houver 100.000 serem inseridas no bd

            dadoG = (line[8].split(",")) #split na coluna 9 (generos do title)
            for i in dadoG:
                    dadosG.append([line[0],i]) #lista de generos de cada title

            if(cont == 100000): #quando alcançar 100.000 registros -> insere com executemany no bd -> limpa as listas e zera o cont
                cont = 0

                cursor.executemany("INSERT INTO TITLES(TCONST,TITLETYPE,PRIMARYTITLE,ORIGINALTITLE,ISADULT,STARTYEAR,ENDYEAR,RUNTIMEMINUTES) VALUES (?,?,?,?,?,?,?,?);",(dadosT))
                conn.commit()
                dadosT = []
                cursor.executemany("INSERT INTO GENRES(TCONST,GENRES) VALUES (?,?);",(dadosG))
                conn.commit()
                dadosG = []

        #insere o resto que não chegou a completar 100.000 registros
        if(dadosT):
            cursor.executemany("INSERT INTO TITLES(TCONST,TITLETYPE,PRIMARYTITLE,ORIGINALTITLE,ISADULT,STARTYEAR,ENDYEAR,RUNTIMEMINUTES) VALUES (?,?,?,?,?,?,?,?);",(dadosT))
            conn.commit()

        if(dadosG):
            cursor.executemany("INSERT INTO GENRES(TCONST,GENRES) VALUES (?,?);",(dadosG))
            conn.commit()

    print("Finalizado insercao de dados de Titles!")
    conn.close()

except sqlite3.Error as error:
    print("Erro em: inserindo dataTitle.tsv", error, line)


#inserindo dados do arquivo tsv de Ratings
try:
    conn = sqlite3.connect('sidia.db')
    print ("DB acessado com sucesso. (inserir Ratings)")
    with open("dataRatings.tsv", encoding='utf-8') as ratingsData:

        print("dataRatings.tsv aberto com sucesso! Iniciando insercao de dados no bd...")
        cursor = conn.cursor()
        next(ratingsData) #Pula primeira linha
        tsvreader = csv.reader(ratingsData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #contador para insercao de dados no banco a cada 100.000 elementos

        dadosR = [] #lista de dados de ratings para serem inseridos no bd ao completar 100.000 elementos

        for line in tsvreader:

            cont = cont + 1

            dadoR = (line[0],line[1],line[2])
            dadosR.append(dadoR) #adiciona linha na lista para quando houver 100.000 serem inseridas no bd

            if(cont == 100000): #quando alcançar 100.000 registros -> insere com executemany no bd -> limpa a lista e zera o cont
                cont = 0

                cursor.executemany("INSERT INTO RATINGS(TCONST,AVERAGERATING,NUMVOTES) VALUES (?,?,?);",(dadosR))
                conn.commit()
                dadosR = []

        #insere o resto que não chegou a completar 100.000 registros
        if(dadosR):
            cursor.executemany("INSERT INTO RATINGS(TCONST,AVERAGERATING,NUMVOTES) VALUES (?,?,?);",(dadosR))
            conn.commit()

    print("Finalizado insercao de dados de Ratings!")
    conn.close()

except sqlite3.Error as error:
    print("Erro em: inserindo dataRatings.tsv", error)


#inserindo dados do arquivo tsv de Names
try:
    conn = sqlite3.connect('sidia.db')
    print ("DB acessado com sucesso. (inserir Names)")
    with open("dataName.tsv", encoding='utf-8') as nameData:

        print("dataName.tsv aberto com sucesso! Iniciando insercao de dados no bd...")
        cursor = conn.cursor()
        next(nameData) #Pula primeira linha
        tsvreader = csv.reader(nameData, dialect='excel-tab',quoting=csv.QUOTE_NONE)

        cont = 0 #contador para insercao de dados no banco a cada 100.000 elementos

        dadosN = [] #lista de dados de names para serem inseridos no bd ao completar 100.000 elementos
        dadosK = [] #lista de dados de knownForTitles para serem inseridos no bd ao completar 100.000 elementos
        dadosP = [] #lista de dados de primaryProfession para serem inseridos no bd ao completar 100.000 elementos

        for line in tsvreader:

            cont = cont + 1

            for i in range(1,6): #onde tiver \N ou "vazio" será salvo como null
                if((line[i] == "\\N") or (len(line[i])) == 0):
                    line[i] = "null";

            dadoN = (line[0],line[1],line[2],line[3])
            dadosN.append(dadoN) #adiciona linha (até a coluna 4) na lista para quando houver 100.000 serem inseridas no bd

            dadoP = (line[4].split(",")) #split na coluna 5 (profissoes do ator)
            for i in dadoP:
                dadosP.append([line[0],i]) #adiciona nconst e profissoes na lista para quando houver 100.000 serem inseridas no bd

            dadoK = (line[5].split(",")) #split na coluna 6 (lista de titulos por quais o ator é conhecido)
            for i in dadoK:
                dadosK.append([line[0],i]) #adiciona nconst e titulos na lista para quando houver 100.000 serem inseridas no bd

            if(cont == 100000): #quando alcançar 100.000 registros -> insere com executemany no bd -> limpa as listas e zera o cont
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

        #insere o resto que não chegou a completar 100.000 registros
        if(dadosN):
            cursor.executemany("INSERT INTO NAMES(NCONST,PRIMARYNAME,BIRTHYEAR,DEATHYEAR) VALUES (?,?,?,?);",(dadosN))
            conn.commit()

        if(dadosP):
            cursor.executemany("INSERT INTO PROFESSIONS(NCONST,PRIMARYPROFESSION) VALUES (?,?);",(dadosP))
            conn.commit()

        if(dadosK):
            cursor.executemany("INSERT INTO KNOWNFORTITLES(NCONST,TCONST) VALUES (?,?);",(dadosK))
            conn.commit()

    print("Finalizado insercao de dados de Names!")
    print("Banco populado com sucesso!")
    conn.close()

except sqlite3.Error as error:
    print("Erro em: inserindo dataName.tsv", error)
