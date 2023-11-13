#!/bin/bash



if [[ ($# -eq 0 ) ]]
then
	echo "Select the container to start"
	i=1
	
	for c in $(docker container ls -a --format '{{.Names}}')
	do
			echo $i $c
			i=$(( $i + 1 ))
	done
	
	read container_index
	i=1
	correct_index=0
	for c in $(docker container ls -a --format '{{.Names}}')
	do
		if [[ $i -eq $container_index ]]
		then
			container_name=$c
			correct_index=1
		fi
		i=$(( $i + 1 ))
	done
	if [[ $correct_index -eq 0 ]]
	then
		echo "[ERROR] no container index recognized, exiting..."
		exit 0
	fi
	
else
	found=0
	for c in $(docker container ls -a --format '{{.Names}}')
		do
			if [ $1 == $c ] 
			then
				container_name=$1
				found=1
			fi
	done
	
	if [[ $found -eq 0 ]]
	then
		echo "[ERROR] required container not present, exiting..."
		exit 0
	fi
fi

echo "Connecting to the container: " $container_name

xhost +

if [ "$( docker container inspect -f '{{.State.Running}}' $container_name )" == "false" ]; 
then 
	echo "start the container: " $container_name	
	docker container start $container_name
fi

docker container  exec -it $container_name bash


