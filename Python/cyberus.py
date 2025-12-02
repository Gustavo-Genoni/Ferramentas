#!/usr/bin/python3

# Ferramenta que realiza portscan utilizando múltiplos threads.
# Criador por: Gustavo Genoni
# Criado em: 2025-12-02

import argparse
import threading
import socket

#   Definindo argumentos

args = argparse.ArgumentParser()
args.add_argument("-t","--threads", help="Define os threads utilizados. Padrão 10",required=False)
args.add_argument("-ip","--ipv4", help="Define o ipv4 do alvo",required=True)
args.add_argument("-p","--porta",help="Define porta alvo",required=False)
args.add_argument("-lp","--listaportas", help="Arquivo com portas",required=False)

argumentos = args.parse_args()

#   Define os threads
if argumentos.threads:
    limitador = threading.Semaphore(int(argumentos.threads))
else:
    limitador = threading.Semaphore(10)


#   Função que faz o scan
def scanner(ip,porta):
    with limitador:
        
        try:
            portaI = int(porta)
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(1)
            resposta = sk.connect_ex((ip,portaI))
        
            if resposta == 0:
                print(f"[CYBERUS] Porta: {porta} - Aberta")
        except:
            pass

        finally:
            sk.close()
            

#    Função que cria os threads e chama scanner
def threads_scanner(ip,portas):
    threads = []

    for porta in portas:

        th = threading.Thread(target=scanner, args=(ip,porta))
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

#    Trata dos argumntos
if argumentos.listaportas:
    try:
        with open(argumentos.listaportas, 'r') as f:
            portas_do_arquivo = [p.strip() for p in f.readlines() if p.strip()]
            threads_scanner(argumentos.ipv4, portas_do_arquivo)
    except FileNotFoundError:
        print(f"Erro: Arquivo de portas '{argumentos.listaportas}' não encontrado.")    
elif argumentos.porta:
    portas = [argumentos.porta]
    threads_scanner(argumentos.ipv4,portas)

else:
    print(f"Erro! nenhuma porta ou lista de portas informada!")
    
