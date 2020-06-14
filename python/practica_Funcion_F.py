"""
Práctica 1 Gestión de empresas
@Author: Samuel Casal Cantero
@Date : 10/10/2019
"""

# IMPORTACIONES DE LAS LIBRERIAS QUE VAMOS A USAR
import os
import random
import time
import math

# Función para leer los ficheros de qeu tenemos en el current work directory


def leerFichero():
    # Declaracion de variables
    n = 0
    f = "Doc1.txt"

    # Nos colocamos en el current working directory, donde tenemos los ficheros
    cwd = os.getcwd()

    # Cogemos todos los ficheros que tenemos en la ruta actual
    files = os.listdir(cwd)

    # Pedimos el valor del nuevo fichero que queremos
    while True:
        # Mostramos una lista de los ficheros que tenemos
        print("*********************************")
        print("****    Lista de Ficheros    ****")
        print("*********************************")
        # Pedimos el nombre del fichero
        for i, fich in enumerate(files):
            print("\t", i, "\t>> ", fich)

        # Ahora recogemos la entrada que queremos
        n = int(input("\nIntroduce el número del fichero con el que deseas trabajar: "))

        # En el caso de que la entrada este dentro de los ficheros salimos del bucle
        if n < 0 or n > len(files):
            print("\nEl numero del fichero no es válido!")
        else:
            break
    # Mostramos el mensaje de que estamos con el fichero n
    print("\nEstas trabajando con el fichero = ", files[n])
    # Declaramos las variables que vamos a devolver
    f = open(files[n])
    matriz = []
    nObjetos = 0
    nMaq = 0

    # Creamos la matriz con los datos que tenemos en el fichero txt
    for i, l in enumerate(f):
        # Cambiamos cada una de las lineas a vector, en vez de que sean un string
        vl = l.split()

        # La primera fila del doc no vale como input del calculo
        if (i == 0):
            nObjetos = int(vl[0])
            nMaq = int(vl[1])
        else:
            # Variable donde metemos cada una de las filas de la matriz
            fila = vl[1::2]
            fila = [int(x) for x in fila]
            matriz.append(fila)

    # Generamos la secuencia de los valores de entrada de los objetos a la máquina y la ramdomizamso
    secuencia = list(range(1, nObjetos+1))
    random.shuffle(secuencia)

    # DEVOLVEMOS LA MATRIZ. SECUENCIA, N_OBJETOS, N_MAQUINAS
    return matriz, secuencia, nObjetos, nMaq, files[n]


def F(secuencia, matriz, nMaq, nObjetos):
    # print("mostramos el valor de secuencia de la linea 79",secuencia)
    tInicial = time.clock()
    R = [[0]*nMaq for _ in range(nObjetos)]

    # Iteramos sobre la matriz de las secuencias
    for i, f in enumerate(secuencia):
        # Ajustamos el indice de las filas de cada objeto porque tiene un desfase de 1
        f = f-1

        # Comprobamos si estamos en el caso inicial
        if i == 0:
            # Iteramos sobre los tiempos del objeto en el que estamos, es este caso f
            for j, t in enumerate(matriz[f]):
                if j == 0:
                    R[f][0] = t
                else:
                    R[f][j] = R[f][j-1]+t

        # En el caso de que no sea el primero de los objetos de secuencia
        else:
            fAnterior = secuencia[i-1]-1
            for j, t in enumerate(matriz[f]):
                if j == 0:
                    R[f][0] = R[fAnterior][j]+t
                else:
                    maximo = max((R[f][j-1], R[fAnterior][j]))
                    R[f][j] = maximo+t
    tFinal = time.clock()
    tEje = (tFinal)-(tInicial)
    #print("Tiempo F = ",tEje*1000, " miliseconds")
    return tEje, R


def F_Med(secuencia, matriz, nMaq, nObjetos):
     # Tenemos que pedir por pantalla el numero de iteraciones que queremos hacer
    entrada = int(input("\tIntroduce el numero de iteraciones: "))
    contador = 0
    media = 0
    mediaDos = 0
    tiempos = 0
    tAux = 0
    while contador != entrada:
        random.shuffle(secuencia)

        if(contador == 0):
            tAux, matrizResultado = F(secuencia, matriz, nMaq, nObjetos)
            tiempos = tiempos + tAux
            columna_ultima = [row[nMaq-1] for row in matrizResultado]

            media = sum(columna_ultima)/nObjetos

        else:
            tAux, matriz_aux = F(secuencia, matriz, nMaq, nObjetos)
            tiempos = tiempos + tAux

            columna_ultima = [row[nMaq-1] for row in matriz_aux]

            mediaDos = sum(columna_ultima)/nObjetos

            if(mediaDos < media):
                matrizResultado = matriz_aux
                media = mediaDos
                secuencia_optima = secuencia

        contador = contador+1

    return media, matrizResultado, secuencia_optima, tiempos


def F_Max(secuencia, matriz, nMaq, nObjetos):
    tAux, matriz_aux = F(secuencia, matriz, nMaq, nObjetos)
    maximo = max(map(max, matriz_aux))
    return maximo, matriz_aux, tAux


def F_Max_Aleatoria(secuencia, matriz, nMaq, nObjetos):
    # Tenemos que pedir por pantalla el numero de iteraciones que queremos hacer
    entrada = int(input("\tIntroduce el numero de iteraciones: "))
    contador = 0
    maximo = 0
    maximoDos = 0
    tiempos = 0
    tAux = 0
    while contador != entrada:
        random.shuffle(secuencia)

        if(contador == 0):
            maximo, matrizResultado, tAux = F_Max(
                secuencia, matriz, nMaq, nObjetos)
            tiempos = tiempos + tAux
        else:
            maximoDos, matriz_aux, tAux = F_Max(
                secuencia, matriz, nMaq, nObjetos)
            tiempos = tiempos + tAux

            if(maximoDos < maximo):
                matrizResultado = matriz_aux
                maximo = maximoDos
                secuencia_optima = secuencia

        contador = contador+1

    return maximo, matrizResultado, secuencia_optima, tiempos


def F_Primer_Mejor(secuencia, matriz, nMaq, nObjetos):
    # Declaramos las variables que vamos a usar
    flagSalida = False  # Flag que indicada la salida del while
    flagStop = False
    tiempo = 0  # Variable donde se recogen los tiempos de ejecucion de F_Local_Mejor
    maximo = 0  # Maximo de control 1
    maximo_auxiliar = 0
    # Copia de la secuencia que iteramos, porque se modifica dentro de los for
    secuencia_copia = []
    secuencia_optima = []  # Secuencia que tenemos que devolver como resultado de la funcion
    contador = 0  # Contador del desfase del segundo for, para que siempre el vecino i itere sobre el siguiente j
    matrizF = []  # Contiene el resultado de cada una de las iteraciones de la secuencia
    matriz_optima = []  # Contiene el resultado de la secuencia optima

    # Controlamos el tiempo inicial
    tiempo_inicial = time.clock()

    # Sacamos el maximo de la secuencia que se nos pasa como valor inicial ya que puede que se nos pase la mejor de las secuencias
    t, matrizF = F(secuencia, matriz, nMaq, nObjetos)
    maximo = max(map(max, matrizF))

    # Hacemos la copia de la secuencia, con list, para que llame al constructor, porque si no es apuntador
    secuencia_copia = list(secuencia)

    # Iniciamos el bucle de la f_Local_Mejor
    while flagSalida == False:

        # Actualizamos el valor de parada y del contador
        flagStop = False
        contador = 0

        # Iteramos sobre el vecino más a la izquierda que vammos a permutar
        for i, valueI in enumerate(secuencia_copia):
            # Aumentamos el contador de control de desfase
            contador = contador + 1

            # Controlamos que el vecino no sea el ultimo, ya que en ese caso no tiene que permutar más
            if i != len(secuencia_copia):

                # Iteramos sobre los vecinos siguientes de i
                for j, valueJ in enumerate(secuencia_copia[i+1:]):

                    # Cambiamos el desfase de j
                    j = j + contador

                    # Cambiamos los vecino i por j en la secuencia
                    secuencia[i] = valueJ
                    secuencia[j] = valueI

                    maximo_auxiliar, matrizF, tAux = F_Max(
                        secuencia, matriz, nMaq, nObjetos)

                    # Miramos si hemos sacado un valor minimo que maximo
                    if(maximo_auxiliar < maximo):

                        # Cambiamos el valor del maximo, es decir, tenemos un nuevo minimo que mejor al max
                        maximo = maximo_auxiliar
                        # Nos quedamos con la secuencia actual
                        secuencia_copia = list(secuencia)
                        # Cambiamos el valor de la matriz optima
                        matriz_optima = [row[:] for row in matrizF]
                        # Cumple el criterio de parada de flagStop
                        flagStop = True
                    else:
                        # Desacemos el cambio para tener la secuencia anterior
                        secuencia = list(secuencia_copia)

                    # Miramos si tenemos criterio de parada de los fors
                    if flagStop == True:
                        break

            # Salimos del primero de los bucles
            if flagStop == True:
                break

        # En el caso de que la secuencia no cambie llegaremos al final del while, por lpo que fStop = false
        if flagStop == False:
            flagSalida = True

        # Nos quedamos con la secuencia optima
        secuencia_optima = list(secuencia)

        # Paramos el tiempo 10 segundo para ver que es lo que pasa
        time.sleep(0)

    tiempo_final = time.clock()

    # Calculamos el valor de duración de la función
    tiempo = tiempo_final-tiempo_inicial
    # Devolvemos los datos necesarios
    return maximo, matriz_optima, secuencia_optima, tiempo

    ##################################################################################


"El que más me gusta"


def F_Mejor_Vecino(secuencia, matriz, nMaq, nObjetos):
    """ Este método se encarga de iterar sobre todos los vecinos, en el caso de que encuentr
    una de las soluciones más optimas se la queda, asi hasta llegar al final de las iteracciones
    de los vecinos
    """
    # Declaramos las variables de control que vamos a usar
    tiempo = 0  # Variable donde se recogen los tiempos de ejecucion de F_Local_Mejor
    maximo = 0  # Maximo de control 1
    maximo_auxiliar = 0
    # Copia de la secuencia que iteramos, porque se modifica dentro de los for
    secuencia_copia = []
    secuencia_optima = []  # Secuencia que tenemos que devolver como resultado de la funcion
    contador = 0  # Contador del desfase del segundo for, para que siempre el vecino i itere sobre el siguiente j
    matrizF = []  # Contiene el resultado de cada una de las iteraciones de la secuencia
    matriz_optima = []  # Contiene el resultado de la secuencia optima

    # Controlamos el tiempo inicial
    tiempo_inicial = time.clock()

    # Sacamos el maximo de la secuencia que se nos pasa como valor inicial ya que puede que se nos pase la mejor de las secuencias
    t, matrizF = F(secuencia, matriz, nMaq, nObjetos)
    maximo = max(map(max, matrizF))

    # Realizamos la copia de la secuencia
    secuencia_copia = list(secuencia)

    for i, valueI in enumerate(secuencia_copia):
            # Aumentamos el contador de control de desfase
        contador = contador + 1

        # Controlamos que el vecino no sea el ultimo, ya que en ese caso no tiene que permutar más
        if i != len(secuencia_copia):

            # Iteramos sobre los vecinos siguientes de i
            for j, valueJ in enumerate(secuencia_copia[i+1:]):
                secuencia = list(secuencia_copia)

                # Cambiamos el desfase de j
                j = j + contador

                # Cambiamos los vecino i por j en la secuencia
                secuencia[i] = valueJ
                secuencia[j] = valueI

                maximo_auxiliar, matrizF, tAux = F_Max(
                    secuencia, matriz, nMaq, nObjetos)

                # Miramos si hemos sacado un valor minimo que maximo
                if(maximo_auxiliar < maximo):

                    # Cambiamos el valor del maximo, es decir, tenemos un nuevo minimo que mejor al max
                    maximo = maximo_auxiliar
                    # Nos quedamos con la secuencia actual, ya que es la ultima de las mejoras
                    secuencia_optima = list(secuencia)
                    # Cambiamos el valor de la matriz optima
                    matriz_optima = [row[:] for row in matrizF]

                    # Volvemos a desacer el cambio
                    secuencia = list(secuencia_copia)

                else:
                    # Desacemos el cambio para tener la secuencia anterior
                    secuencia = list(secuencia_copia)

    # En el caso de que no tengamos secuencia optima es la de entrada
    if secuencia_optima == []:
        secuencia_optima = list(secuencia_copia)
    tiempo_final = time.clock()

    # Calculamos el valor de duración de la función
    tiempo = tiempo_final-tiempo_inicial
    # Devolvemos los datos necesarios
    return maximo, matriz_optima, secuencia_optima, tiempo


"""Función de recocido simulado
    @params:
        t_inicial:  temperatura por la que empezamos a hacer el recocido
        numIntentos: numero de intentos que se hacen en cada una de las iteraccione del recocido
        t_final:    temperatura de parada, es decir, se para cuando t_incial se hace menor que t_final
        secuecia:   entrada de los objetos en las máquinas
        matriz:     matriz de los objetos y sus tiempos en cada máquina
"""


def recocido_Fmax(t_inicial, numIntentos, t_final, matriz, secuencia, nMaq, nObjetos):
    if t_final > t_inicial:
        return None

    # Comenzamos a calcular el tiempo inicial
    tiempo_inicial = time.clock()

    # Recogemos el valor de tiempo incinial en t
    t = int(t_inicial)

    # Generamos una nueva sol con Fmax(), algunas de los valores retornados no se llegan a usar
    mejor_secuencia = list(secuencia)
    random.shuffle(mejor_secuencia)
    maximo_mejor, matriz_sol, tAux = F_Max(
        mejor_secuencia, matriz, nMaq, nObjetos)
    contador = 0
    print("Ejecutando --> ", sep=' ', end='', flush=True)
    # Entramos dentro del bucle while, siempre que tengamos un tempo mayor que el de parada
    while t >= t_final:
        print("#", sep='', end='', flush=True)
        contador = contador + 1
        nuevo_num_intentos = int(int(t)/(3.141529*3.141529))
        # Hacemos tantas pruebas como numero De intentos * la temperatura, ya que los intentos se van enfriando
        for x in range(nuevo_num_intentos):

            # Debemos de sacar los valores de i j para hacer el cambio de la matriz
            i = int(random.uniform(0, nObjetos-1))
            j = int(random.uniform(0, nObjetos-1))

            while j == i:
                j = int(random.uniform(0, nObjetos-1))

            # Cogemos los valores de la secuencia en cada una  de las posiciones
            valor_i = mejor_secuencia[i]
            valor_j = mejor_secuencia[j]

            # Cambiamos los valores
            mejor_secuencia[i] = valor_j
            mejor_secuencia[j] = valor_i
            prueba_secuencia = list(mejor_secuencia)

            # Desacemos los cambios de la permutacion
            mejor_secuencia[j] = valor_j
            mejor_secuencia[i] = valor_i
            mejor_secuencia = list(mejor_secuencia)

            # Calculamos con f_Max() un nuevo valor maximo
            maximo_prueba, matriz_prueba, tAux = F_Max(
                prueba_secuencia, matriz, nMaq, nObjetos)

            # Sacamos el valor de delta
            delta = maximo_prueba - maximo_mejor

            # En el caso de que delta este sea menor que cero, es que tenemos mucha mejora o que por azar  se cunpla los sigueinte
            if delta < 0 or random.uniform(0, 1) < math.e**(-delta/t):

                # En el caso de que tengamos alguna mejor hacemos la prueba del mejor vecino para mejorar la secuencia
                maximo_mejor, matriz_final, secuencia_mas_mejor, duracion = F_Mejor_Vecino(
                    mejor_secuencia, matriz, nMaq, nObjetos)
                mejor_secuencia = list(secuencia_mas_mejor)

        # Sacamos un nuevo valor de t, ya que la temeparatura debe de ir bajando, enfriando
        t = int(t*(0.80))

    # Hacemos una busqueda de primer mejor a la salida para validar de que tneemos la mejor solucion de la solucion
    maximo_Final, matriz_final, secuencia_final, duracion = F_Mejor_Vecino(
        mejor_secuencia, matriz, nMaq, nObjetos)

    # Sacamos los valores de los tiempos para devolverllos
    tiempo_fin = time.clock()
    tiempo_total = tiempo_fin-tiempo_inicial
    print("\n")
    #print("contador = ",contador)
    return maximo_Final, matriz_final, secuencia_final, tiempo_total


def genetico(secuencia, matriz, nMaq, nObjetos):
    # Declaracion de variables
    maximo = float('inf')
    secuencia_maximo = []
    poblacion = []
    maximos_poblacion = []
    contador = 0
    tiempo_inicial = time.clock()
    pila = []
    
    """CREACIÓN DE LA POBLACIÓN INICIAL"""
    # Lo primero que tenemos que hacer es definir una poblacion inicial de secuencias de pruebas, en este caso de 100 individuos
    for i in range(1001):
        # Generamos una nueva secuencia laeatoria y se la añadimos a la lista poblacion
        random.shuffle(secuencia)
        poblacion.append(list(secuencia))

        # Generamos el maximo para cada una de las secuencias y lo guardamos en máximos
        m, matriz_matrix_sol, t = F_Max(secuencia, matriz, nMaq, nObjetos)
        maximos_poblacion.append(m)

        # Miramos que el nuevo maximo es menor que el maximo que tenemos guardado
        if m < maximo:
            maximo = m
            secuencia_maximo = list(secuencia)


    while contador<1000:
        """RELLENMOS EL VECTOR DE LOS PADRES CON TORNEO ALEATORIO"""
        padres = []
        for i in range(1000):
            # Generamos los valores aleatorios para coger dos padres
            
            # CHOICCE MIRAR
            x = random.randint(0, 999)
            y = random.randint(0, 999)
            while x is y:
                y = random.randint(0, 999)
                
            
            # Hacemos el torneo para ver quien de los dos es el mejor
            maximo_x = maximos_poblacion[x]
            maximo_y = maximos_poblacion[y]
            
            if maximo_x>=maximo_y:
                padres.append(poblacion[x])
            else:
                padres.append(poblacion[y])
                
        # Mostramos el vector de los padres 
        
        
        # for i in range(100):
            #print("\t",padres[i])
            
        """A PARTIR DE LOS PADRES SACAMOS EL VECTOR DE LOS HIJOS CON LAS MUTACIONES, HASTA QUE TENGAMOS 100 HIJOS"""
        hijos = []
        maximos_hijos = []
        for i in range(700):
            
            # Mediante cruce_OX, debemos de sacar dos padres aleatorios
            if i<=299:
                x = random.randint(0, 999)
                y = random.randint(0, 999)
                while x is y:
                    y = random.randint(0, 999)
            
                p = padres[x]
                m = padres[y]
                
                # HAcemos los crucess_OX
                hijo_PM = cruce_OX(p,m,nObjetos)
                hijo_MP = cruce_OX(m,p,nObjetos)  
                
                # Metemos los hijos en el vector de los hijos
                hijos.append(hijo_PM)
                m, matriz_matrix_sol, t = F_Max(hijo_PM, matriz, nMaq, nObjetos)
                maximos_hijos.append(m)
                hijos.append(hijo_MP)
                m, matriz_matrix_sol, t = F_Max(hijo_MP, matriz, nMaq, nObjetos)
                maximos_hijos.append(m)
            else:
                x = random.randint(0, 999)
                p = padres[x]
                p_mutado = list(mutador(p,nObjetos))
                hijos.append(p_mutado)
                m, matriz_matrix_sol, t = F_Max(p_mutado, matriz, nMaq, nObjetos)
                maximos_hijos.append(m)
                
        # Una vez terminamos de hacer los hijos metemos el mejor de las secuencias
        hijos.append(secuencia_maximo)
        
        maximos_hijos.append(maximo)
        
        # Cambiamos las variables
        poblacion = []
        poblacion = list(hijos)
        
        hijos = []
        maximos_poblacion = []
        maximos_poblacion = list(maximos_hijos) 
        maximos_hijos = []
        padres = []
        contador = contador +1

        # Cogemos de la poblacion el menor de todos, es decir, el mejor
        index_mejor = maximos_poblacion.index(min(maximos_poblacion))
        
        maximo = maximos_poblacion[index_mejor]
        secuencia_maximo = poblacion[index_mejor]
        
        maximo_mejor, matriz_final, secuencia_mas_mejor, duracion = F_Mejor_Vecino(
                    secuencia_maximo, matriz, nMaq, nObjetos)
        
        maximo = maximo_mejor
        secuencia_maximo = secuencia_mas_mejor
        
        poblacion[index_mejor] = secuencia_mas_mejor
        maximos_poblacion[index_mejor] = maximo_mejor
        
        # Controlamos la parada 
        pila.append(maximo)
        if len(pila) > 10:
            
            if(len(set(pila[-3:]))==1):
                # Salimos del while
                break
        print("MAXIMO = ",maximo)
        
    print("El valor minimo es ",maximo," para la secuencia ",secuencia_maximo )
    tiempo_fin = time.clock()
    tiempo_total = tiempo_fin-tiempo_inicial
    
    print("El tiempo total es  = ",tiempo_total)

def cruce_OX(p, m, nObjetos):
    m_aux = []
    corte = random.randint(0, (int(nObjetos/2)-1))
    half_P = p[corte:(corte+int(nObjetos/2))]
    set_half_P = set(half_P)

    # Sacamos los valores de la madre en orden que no estan en el half_P
    for i, value in enumerate(m):
        if value not in set_half_P:
            m_aux.append(value)

    # Añadimos por el principio valores hasta el corte
    for i in range(corte):
        half_P.insert(0, m_aux.pop())

    # Añadimos lo que queda hasta el final
    half_P.extend(m_aux)

    devolver = list(mutador(half_P,nObjetos))
    return devolver

def mutador(secuencia,nObjetos):
    # Debemos de generar un número entre 0 y 1 para saber si se produce la mutación, porque no siepre
    probabilidad = random.random()
    
    # Miramos si la prob esta en el 75%, entonces no se porduce mutacion, si no si
    if probabilidad <0.75:
        return secuencia
    
    # cada uno de los hijos va a tener una permutaacion aleatoria
    x = random.randint(0, nObjetos-1)
    y = random.randint(0, nObjetos-1)
    while x is y:
        y = random.randint(0, nObjetos-1)

    value_x = secuencia[x]
    value_y = secuencia[y]
    secuencia[x] = value_y
    secuencia[y] = value_x
    
    return secuencia

def menu():

    os.system('cls')
    # Primero pedimos los datos que vamos a usar para todo el ejercicio
    matriz, secuencia, nObjetos, nMaq, fichero = leerFichero()

    # Limpiamos el contenido de la consola
    os.system('cls')

    opcion = 100
    while opcion != 0:
        print("\n***************************************************")
        print("*******************    MENÚ    *******************")
        print("***************************************************")
        print("\t\t\t Fichero --> ", fichero)
        print("***************************************************")
        print("*\t1 - Cambiar fichero                       *")
        print("*\t2 - Función F()                           *")
        print("*\t3 - Función F_Med_Aleatoria()             *")
        print("*\t4 - Función F_Max_Aleatoria()             *")
        print("*\t5 - Función F_Primer_Mejor()              *")
        print("*\t6 - Función F_Mejor_Vecino()              *")
        print("*\t7 - Función Recocido_Simulado()           *")
        print("*\t8 - Función Genetico()                    *")
        print("*\t0 - salir                                 *")
        print("***************************************************")
        opcion = int(input("\nIntroduce el valor de la opción deseada: "))
        if(opcion > 8 or opcion < 0):
            print("\nEl valor de la opción introducida no es un valor dentro del rango!")
        else:
            if opcion == 1:
                matriz, secuencia, nObjetos, nMaq, fichero = leerFichero()
                print("\nFichero cambiado a ", fichero)
            elif opcion == 2:
                print("\n\tFUNCION F()")
                print("\t***************")
                secuenciaEjemplo1 = [4, 1, 3, 5, 2]
                secuenciaDoc1 = [9, 4, 1, 2, 8, 3, 10, 7, 5, 11, 6]
                t, sol = F(secuencia, matriz, nMaq, nObjetos)
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tSecuencia aleatoria ", secuencia)
                for f in sol:
                    print("\t", f)
            elif opcion == 3:
                print("\n\tFUNCION F_Med()")
                print("\t*****************")
                media, sol, secuencia, t = F_Med(
                    secuencia, matriz, nMaq, nObjetos)
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tMedia = ", media, ", secuencia óptima= ", secuencia)
                for f in sol:
                    print("\t", f)
            elif opcion == 4:
                print("\n\tFUNCION F_Max()")
                print("\t***************")
                maximo, sol, secuencia, t = F_Max_Aleatoria(
                    secuencia, matriz, nMaq, nObjetos)
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tMaximo = ", maximo, ", secuencia óptima= ", secuencia)
                for f in sol:
                    print("\t", f)
            elif opcion == 5:
                secuencia5 = [4, 1, 6, 5, 7, 8, 2, 3]
                secuenciad1 = [3, 11, 9, 10, 5, 6, 8, 7, 4, 5, 1]
                print("\n\tFUNCION F_Primer_Mejor()")
                print("\t**************************")
                maximo, sol, sec_op, t = F_Primer_Mejor(
                    secuencia, matriz, nMaq, nObjetos)
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tMaximo = ", maximo, ", secuencia óptima= ", sec_op)
                for f in sol:
                    print("\t", f)
            elif opcion == 6:
                print("\n\tFUNCION F_Mejor_Vecino()")
                print("\t**************************")
                secuenciad1 = [6, 3, 11, 7, 8, 5, 1, 2, 4, 9, 10]

                maximo, sol, sec_op, t = F_Mejor_Vecino(
                    secuencia, matriz, nMaq, nObjetos)
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tMaximo = ", maximo, ", secuencia óptima= ", sec_op)
                for f in sol:
                    print("\t", f)
            elif opcion == 7:
                print("\n\tFUNCION recocido_Fmax()")
                print("\t*****************************")

                maximo, matriz_aux, tAux = F_Max(
                    secuencia, matriz, nMaq, nObjetos)

                # Sacamos el valor de la t inicial
                temp_inicial = maximo*(0.4)
                maximo, sol, sec_op, t = recocido_Fmax(
                    temp_inicial, 50, 1, matriz, secuencia, nMaq, nObjetos)

                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
                print("\tMaximo = ", maximo, ", secuencia óptima= ", sec_op)
                for f in sol:
                    print("\t", f)
            elif opcion == 8:
                print("\n\tFUNCION genetico()")
                print("\t*****************************")

                # Sacamos el valor de la t inicial
                genetico(secuencia, matriz, nMaq, nObjetos)
                t = 0
                print("\tTiempo ejecucion fichero =",
                      fichero, " -->", t, " segundos.")
            elif opcion == 0:
                print("\n\n SALIENDO!!!")


menu()