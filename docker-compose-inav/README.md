# Complete Guide to Setting up SITL (Software-in-the-Loop) Environment for Drones using Docker and INAV

This guide provides step-by-step instructions for creating and running this environment.

## Structure of the 'environment

![]([struttura](https://github.com/NS-unina/GCAP_Mod/blob/main/docker-compose-inav/screen/Structure.png))

## Download Inav-Configurator for your macchiana(the link below is for mac machine)

```
   https://github.com/iNavFlight/inav-configurator/releases/download/6.1.0/INAV-Configurator_macOS_6.1.0.dmg

```

General repo link: https://github.com/iNavFlight/inav-configurator/releases

## Download the repository and navigate to the folder docker-compose-inav

```
   git clone https://github.com/NS-unina/GCAP_Mod.git
   cd ~/docker-compose-inav
```

## Run build command

```
docker-compose build 
```

## Run up command

```
docker-compose up -d

```

## Launch docker exec for each container one for views in the terminal

```
   1. docker exec -ti flight_controller bash
   2. docker exec -ti gps bash

```

## Continue to the relevant directories into flight_controller container

```
1. cd ~/cd inav-6.1.1/build_SITL
```

## Startup command for flight_controller.

```
1. ~./inav_6.1.1_SITL
```

![](flightcontroller)

After starting the flight_controller open Inav-Configurator on your computer

## Inav-Configurator

Follow the image to set the environment correctly

![](inav-Configurator)
![](Istruzioni 1)
![](Istruzioni 2)
![](TCP_port)
![](tutte le immagini restanti)

After completing the setup let's move to the gps-related docker terminal

## Before starting the gps script you need to edit the code and enter the correct ip related to the docker network

Follow steps

```
1. Open a new terminal and run this command to verify the ip address
2.  docker inspect fligh_controller
```

![](Dockeri_nspect)

## Gps terminal

Return to the gps terminal and run these commands

```
1. ~./micro gps_nmea_SGTD_FG.py

```

Change ip and port

![](microgps)

```
2. ~./python3 gps_nmea_SGTD_FG.py

```

![](python3 gps)

## Results on Inav-Configurator

![](Risultati)

![](git)
