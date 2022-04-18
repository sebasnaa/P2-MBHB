
import itertools
import random
import algoritmos 

import numpy as np


def genera_lista_indices(k):
    lista_sub_indice = []
    r = random.randint(0, 15)
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
    # print(numero_parejas)
    # print(lista_indices_modificar)
    
    for i in range(numero_parejas):
        a = random.choice(lista_indices_modificar)
        b = random.choice(lista_indices_modificar)
       
        while(a == b):
            a = random.choice(lista_indices_modificar)
            b = random.choice(lista_indices_modificar)
        
        # print( "indices ", a , "   " , b)
        if ( np.random.uniform(0,1) > 0.5):
            if(s_inicial[a] > paso_mutacion):
                s_inicial[a] = s_inicial[a] - paso_mutacion
                s_inicial[b] = s_inicial[b] + paso_mutacion
                
            elif (s_inicial[b] > paso_mutacion):
                s_inicial[b] = s_inicial[b] - paso_mutacion
                s_inicial[a] = s_inicial[a] + paso_mutacion
            # print("Valores indice A " ,a , "  ",b)
        else:
            if(s_inicial[b] > paso_mutacion):
                s_inicial[b] = s_inicial[b] - paso_mutacion
                s_inicial[a] = s_inicial[a] + paso_mutacion
            elif (s_inicial[a] > paso_mutacion):
                s_inicial[a] = s_inicial[a] - paso_mutacion
                s_inicial[b] = s_inicial[b] + paso_mutacion
            # print("Valores indice  B " ,a , "  ",b)
            
            
    # k = 0
    # while(k<len(lista_indices_modificar)):
    #     if s_inicial[lista_indices_modificar[k]] == s[lista_indices_modificar[k]]:
    #         print("Valores no modificados")
    #         break
    #     k+=1
        
    return s_inicial
        
   

    
    
def VNS():
    S = algoritmos.greedy_inicializar(16,220)
    k = 1
    S_vecino = S.copy()
    coste_actual = algoritmos.coste_slot(S)
    while k <= 4:
        s_tmp,coste_tmp = algoritmos.busqueda_local(S_vecino)
        print(s_tmp)
        print(S)
        print("Costes " , coste_tmp , "   " , coste_actual , "   k actual ", k)
        if coste_tmp < coste_actual:
            print("Mejora")
            # print("Mejora    Costes -> " ,coste_tmp  , "   " , coste_actual , "   " , k)
            S = s_tmp.copy()
            coste_actual = coste_tmp
            k = 1
        else:
            print("No mejora")
            k +=1
        # Generacionnde vecino por mutacion
        S_vecino = mutar(S,k,2)
        
    print("Solucion BL " , S , " con coste -> ", coste_actual, "   " ,np.array(S).sum() )


s = [36, 10, 13, 16, 15, 10, 12, 11, 14, 12, 12, 16,  7, 12, 16,  8,]
VNS()


# s_actual = mutar(s,1,2)