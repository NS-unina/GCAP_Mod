# Complete Guide to Setting up SITL (Software-in-the-Loop) Environment for Drones using Docker and INAV

This guide provides step-by-step instructions for creating and running this environment.

## The structure of the environment

![struttura](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Structure.png)

## Download Inav-Configurator for your machine(the link below is for mac machine)

```
   https://github.com/iNavFlight/inav-configurator/releases/download/6.1.0/INAV-Configurator_macOS_6.1.0.dmg

```

General repo link: https://github.com/iNavFlight/inav-configurator/releases

## Download the repository and navigate to the folder docker-compose-inav

```
   git clone https://github.com/NS-unina/GCAP_Mod.git
   cd ~/INAV_Flight_controller/docker-compose-inav
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
   3. docker exec -ti radio_command bash
```

## Continue to the relevant directories into flight_controller container

```
1. cd ~/inav-6.1.1/build_SITL
```

## Startup command for flight_controller.

```
1. ./inav_6.1.1_SITL
```

![flightcontroller](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Flight_Controller.png)

After starting the flight_controller open Inav-Configurator on your computer

## Inav-Configurator

Open Inav-Configurator on your machine and follow the image to set the environment correctly

![inav-Configurator](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Inav-Configurator_1.png)
![Istruzioni 1](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/inav-Configurator_2.png)
![TCP_port](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/TCP_port.png)
![Istruzioni 2](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/inav_Conf_final.png)
![](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricopter.png)
![](<[https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricopter.png](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricopter1_1.png)>)
![](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricpoter1_2.png)
In step 7 choose gps and 9600 and click save and reboot
![](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricpoter1_3.png)
Enable gps for navigation and telemetry and Galileo set and change protocol to NMEA and finally save and reboot
![](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Quadricpoter1_4.png)
Now the Gps will enable and it will be red because it is not receiving any data

After completing the setup let's move to the gps-related docker terminal

## Gps terminal

Return to the gps terminal and run these commands

```
1.  python3 gps_nmea_SGTD_FG.py

```

![python3 gps](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/python3gps.png)

## Results on Inav-Configurator

![Risultati](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Risultati.png)
You can see that after launching the script in python the gps turned blue, this indicates that it is receiving data and the result you can see the real time on Inav-Configurator.
Below is a gif extracted from the program

![gif](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/Gifgps.gif)
