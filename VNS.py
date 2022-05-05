
import itertools
import random
import time
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
    
    
    for i in range(k):
        a = random.choice(lista_indices_modificar)
        b = random.choice(lista_indices_modificar)
       
        while(a == b):
            a = random.choice(lista_indices_modificar)
            b = random.choice(lista_indices_modificar)
        
        if ( np.random.uniform(0,1) > 0.5):
            if(s_inicial[a] > paso_mutacion):
                s_inicial[a] = s_inicial[a] - paso_mutacion
                s_inicial[b] = s_inicial[b] + paso_mutacion
                
            elif (s_inicial[b] > paso_mutacion):
                s_inicial[b] = s_inicial[b] - paso_mutacion
                s_inicial[a] = s_inicial[a] + paso_mutacion
        else:
            if(s_inicial[b] > paso_mutacion):
                s_inicial[b] = s_inicial[b] - paso_mutacion
                s_inicial[a] = s_inicial[a] + paso_mutacion
            elif (s_inicial[a] > paso_mutacion):
                s_inicial[a] = s_inicial[a] - paso_mutacion
                s_inicial[b] = s_inicial[b] + paso_mutacion
            
        
    return s_inicial
        
   

    
    
    
   # pendiente agregar la condicion que esta en el usb importante 
def VNS():
    start_time = time.time()
    # S = algoritmos.greedy_inicializar(16,220)
    S = algoritmos.estado_inicial_random()
    k = 1
    bl = 0
    S_vecino = S.copy()
    coste_actual = algoritmos.coste_slot(S)
    while bl < 10:
        print("Valor de bl ", bl)
        s_tmp,coste_tmp = algoritmos.busqueda_local(S_vecino)
        bl += 1
                           
        print(s_tmp, " ", s_tmp.sum())
        print(S , "  ", S.sum())
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
            k = k % 5
        # Generacionnde vecino por mutacion
        S_vecino = mutar(S,k,3)
        
    print("Solucion BL " , S , " con coste -> ", coste_actual, "   " ,np.array(S).sum() , "--- %s seconds ---" % (time.time() - start_time))


s = [36, 10, 13, 16, 15, 10, 12, 11, 14, 12, 12, 16,  7, 12, 16,  8,]
VNS()


# s_actual = mutar(s,1,2)