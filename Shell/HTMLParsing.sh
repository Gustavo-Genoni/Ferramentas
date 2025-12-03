#!/bin/bash

if [ "$1" == "" ]; then
	echo -e "Erro de sintaxe! Modo de uso:\n $0 <url>"
else
	# Banner colorido
	COR_VERDE="\e[32m"
	COR_AMARELA="\e[33m"
	COR_ROXA="\e[35m"
	RESET="\e[0m"	

	#Variaveis do sistema
	DIRETORIO="/tmp/parshtml"
echo -e $COR_ROXA
	cat << "EOF"

$$$$$$$\   $$$$$$\  $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$\      $$\ $$\       
$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ |  $$ |\__$$  __|$$$\    $$$ |$$ |      
$$ |  $$ |$$ /  $$ |$$ |  $$ |$$ /  \__|$$ |  $$ |   $$ |   $$$$\  $$$$ |$$ |      
$$$$$$$  |$$$$$$$$ |$$$$$$$  |\$$$$$$\  $$$$$$$$ |   $$ |   $$\$$\$$ $$ |$$ |      
$$  ____/ $$  __$$ |$$  __$$<  \____$$\ $$  __$$ |   $$ |   $$ \$$$  $$ |$$ |      
$$ |      $$ |  $$ |$$ |  $$ |$$\   $$ |$$ |  $$ |   $$ |   $$ |\$  /$$ |$$ |      
$$ |      $$ |  $$ |$$ |  $$ |\$$$$$$  |$$ |  $$ |   $$ |   $$ | \_/ $$ |$$$$$$$$\ 
\__|      \__|  \__|\__|  \__| \______/ \__|  \__|   \__|   \__|     \__|\________|
                                                                                   
                                                                                                                                                                      
EOF
	echo -e "${COR_AMARELA} Iniciando o parsing no algo: ${1}"

	# | grep "href" | awk -F'href' '{print $2}' | sed "s/=\"//g" | egrep "^http" | awk -F'\">' '{print $1}'
	
	#Verifica o diretório do programa
	if [ -d $DIRETORIO ]; then
		echo "Iniciando..."
		dire=true
	else
		mkdir -p $DIRETORIO 
		echo "iniciando..."
		dire=true
	fi

	if [ $dire ]; then
		NOME_ARQUIVO=`date +"%Y-%m-%d_%H-%M-%S"`
		DIRARQUIVO=$DIRETORIO/$NOME_ARQUIVO

		wget -O $DIRARQUIVO $1 >/dev/null 2>&1

		URLS=`cat $DIRARQUIVO | grep "href" | awk -F'href' '{print $2}' | sed "s/=\"//g" | egrep "^http" | cut -d " " -f 1 | awk -F'/>||">' '{print $1}'`

		echo -e "
		############### RESULTADOS ###############\n
		${COR_VERDE} ${URLS}
		${COR_AMARELA}############### ARQUVOS S. ###############\n
		${COR_VERDE} ${DIRARQUIVO}
		"
	fi


fi
