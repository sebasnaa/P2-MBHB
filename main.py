
import itertools
import random
import algoritmos 

import numpy as np


def genera_lista_indices(k):
    lista_sub_indice = []
    r = random.randint(0, 16)
    longitud = k * 4
    indice = r
    for i in range(longitud):
        lista_sub_indice.append(indice)
        indice = (indice+1) % 16

    return lista_sub_indice

def mutar(s,k,paso_mutacion):
    
    s_inicial = s.copy()
    
    lista_indices_modificar = genera_lista_indices(k)
    parejas_mutaciones = list(itertools.permutations(lista_indices_modificar, 2))
    numero_parejas = int(len(parejas_mutaciones)*0.6)
    print(numero_parejas)
    print(lista_indices_modificar)
    
    for i in range(numero_parejas):
        a = random.choice(lista_indices_modificar)
        b = random.choice(lista_indices_modificar)
       
        while(a == b):
            a = random.choice(lista_indices_modificar)
            b = random.choice(lista_indices_modificar)
        
        
        if ( np.random.uniform(0,1) > 0.5):
            if(s[a] > paso_mutacion):
                s[a] = s[a] - paso_mutacion
                s[b] = s[b] + paso_mutacion
                
            elif (s[b] > paso_mutacion):
                s[b] = s[b] - paso_mutacion
                s[a] = s[a] + paso_mutacion
            # print("Valores indice A " ,a , "  ",b)
        else:
            if(s[b] > paso_mutacion):
                s[b] = s[b] - paso_mutacion
                s[a] = s[a] + paso_mutacion
            elif (s[a] > paso_mutacion):
                s[a] = s[a] - paso_mutacion
                s[b] = s[b] + paso_mutacion
            # print("Valores indice  B " ,a , "  ",b)
            
    k = 0
    while(k<len(lista_indices_modificar)):
        if s_inicial[lista_indices_modificar[k]] == s[lista_indices_modificar[k]]:
            print("Valores no modificados")
            break
        k+=1
    print(s_inicial)
    print(s)
        
    return s
        
   

    
    
def VNS():
    # s_actual = algoritmos.estado_inicial_random()
    s_actual = algoritmos.greedy_inicializar(16,220)
    k = 1
    while k <= 2:
        s_tmp,coste_tmp,coste_actual = algoritmos.busqueda_local(s_actual)
        print("Costes " , coste_tmp , "   " , coste_actual)
        if coste_tmp < coste_actual:
            # print(s_actual ,"\n" , s_tmp)
            s_actual = s_tmp
            k = 1
            print("Costes -> " , coste_actual , "   " , coste_tmp)
        else:
            print("No mejora")
            k +=1
            
        s_actual = mutar(s_actual,k)
    print("Solucion BL " , s_actual , " con coste -> ", coste_actual, "   " ,np.array(s_actual).sum() )


s = [36, 10, 13, 16, 15, 10, 12, 11, 14, 12, 12, 16,  7, 12, 16,  8,]



# VNS()
s_mutada = mutar(s,1,2)



