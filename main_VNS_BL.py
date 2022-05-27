
import itertools
import random
import time
import algoritmosV2

import numpy as np



def calculo_greedy_inicial(solucion_inicial,alpha=5):
    
    sol_mod = algoritmosV2.inicializar_greedy(solucionInicial=solucion_inicial,limite_bicicletas=220)
    
    coste = algoritmosV2.coste_slot(sol_mod)
    total = np.array(sol_mod).sum()
    coste_mod = coste
    if(total > 205):
        coste_mod = (total - 205)*alpha + coste
    
    print(coste_mod)
    

def busqueda_local_mod(alpha=5):
    
    sol_inicial = algoritmosV2.greedy_inicializar(16,233)
    
    sol_final,coste = algoritmosV2.busqueda_local(sol_inicial)
    total = np.array(sol_final).sum()
    coste_mod = coste
    if(total > 205):
        coste_mod = (total - 205)*alpha + coste
    
    print("mod")
    print(sol_final , " ", coste_mod)
    print(sol_final.sum())
    return sol_final,coste_mod
    

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
        
   

def VNS(alpha = 5):
    start_time = time.time()
    S = algoritmosV2.greedy_inicializar(16,233)
    # S = algoritmos.estado_inicial_random()
    k = 1
    bl = 0
    S_vecino = S.copy()
    coste_actual = algoritmosV2.coste_slot(S)
    
    llamadas_total = 0
    
    while bl < 4:
        s_tmp,coste_tmp,llamadas = algoritmosV2.busqueda_local(S_vecino)
        llamadas_total += llamadas
        bl += 1
        # print(bl)
                           
     
        if coste_tmp < coste_actual:
            S = s_tmp.copy()
            coste_actual = coste_tmp
            k = 1
        else:
            k +=1
            k = k % 5
        S_vecino = mutar(S,k,3)
        
    total = np.array(S).sum()  
    if(total > 205):
        coste_mod = (total - 205)*alpha + coste_actual
    else:
        coste_mod = coste_actual
      
    print("Solucion BL " , S , " con coste -> ", coste_mod, "   " ,np.array(S).sum() , "--- %s seconds ---" % (time.time() - start_time))
    print(llamadas_total , " llamadas total coste")


random.seed(258741369)
np.random.seed(258741369)

# random.seed(132456987)
# np.random.seed(132456987)


VNS(alpha=5)
# busqueda_local_mod(alpha=5)



# s_ini = [5,7,13,6,8,13,8,9,6,10,10,18,8,13,15,14]
# calculo_greedy_inicial(s_ini)