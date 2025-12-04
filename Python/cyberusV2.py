#!/usr/bin/python3

BANNER = r"""
                            /\_/\____,
                  ,___/\_/\ \  ~     /
                  \     ~  \ )   XXX
                    XXX     /    /\_/\___,
                       \o-o/-o-o/   ~    /
                        ) /     \    XXX
                       _|    / \ \_/
                    ,-/   _  \_/   \
                   / (   /____,__|  )
                  (  |_ (    )  \) _|
                 _/ _)   \   \__/   (_
                  (,-(,(,(,/      \,),),)

                     C Y B E R U S
                     S C A N N E R
"""



print(BANNER)


#   Importações
import sys
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

#---------------
#   Argumentos
#---------------

parse = argparse.ArgumentParser(description="CYBERUS - PORT SCANNER")

parse.add_argument("-t","--threads",help="Número de threads (Padrão: 50)",required=False)
parse.add_argument("-ip","--ipv4",help="IP ou domínio alvo",required=True)
parse.add_argument("-lp","--listaportas",help="Arquivo contendo portas",required=False)
parse.add_argument("-p","--porta",help="Porta única do alvo",required=False)

argumentos = parse.parse_args()

#---------------
#   Threads
#---------------

if  argumentos.threads:
    max_threads = int(argumentos.threads)
else:
    max_threads = 50



#---------------
#   Scanner
#---------------

def scanner(ip,porta):
    try:
        portaI = int(porta)
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(2)

        resposta = sk.connect_ex((ip,portaI))

        if resposta == 0:
            print(f"\n[CYBERUS]: Porta {portaI} - Aberta")
    except:
        pass

    finally:
        sk.close()



#---------------
#   Threads
#---------------

def threads_scanner(ip,portas):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
    
        for porta in portas:
            executor.submit(scanner, ip, porta)




#---------------
#   DNS 
#---------------

try:
    alvo = socket.gethostbyname(argumentos.ipv4)
except:
    print(f"[CYBERUS]: Erro! Não foi possível resolver o domínio informado\n")
    exit(1)



#---------------
#   Principal
#---------------


if argumentos.listaportas:
    try:
        with open(argumentos.listaportas, "r") as f:
            portas = [linha.strip() for linha in f.readlines() if linha.strip()]
            threads_scanner(alvo, portas)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{argumentos.listaportas}' não encontrado.")

elif argumentos.porta:
    threads_scanner(alvo, [argumentos.porta])

else:
    print("[ERRO] Nenhuma porta informada.")
