## After the overall configuration we move on to the security of the enviroment

## 1. Software Attack

The first step is to change the INAV gps configuration

## Modify Inav-Configurator

In step 18, opt for "Enable MSP" and proceed to save and restart. This action is illustrated in the following screenshot:

![Step 18: Enable MSP](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/attack1.png)

Following the activation of MSP, proceed to enable GPS for navigation and telemetry in the subsequent step. Configure Galileo settings and switch the protocol to MSP. Conclude by saving and restarting the system. This process is visually represented in the following screenshot:

![GPS Configuration: Enable GPS, Set Up Galileo, Change Protocol](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/attack2.png)

Once the GPS configuration is completed, navigate to the "Receiver" tab. Adjust the receiver mode to MSP, then click 'Save and Restart' to implement the changes seamlessly.
![](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/screen/setrc.png)

## Launching docker exec for the Attacker container in a dedicated terminal

```
   1. docker exec -ti attack bash

```

![Container attack](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/attack_terminale_3.png)

## Gps terminal

After the complete setting of Inav and the attacker container we return to the gps terminal and run this command for start the mission

```
1. python3 missioneMSP.py  --ip 172.18.0.2 --port 5762 --file gps_coordinate_missione.txt

```

The result of INAV receiving of the mission
![Screen missione coordinate MSP](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/CoordinateGPS_misisone_MSP.png)

## Attacker terminal for gps attack

Move to the attacker terminal and launch this command to complete the attack

```
1. python3 attackMSP.py --ip 172.18.0.2 --port 5761 --file Coordinate_Attacco.txt

```

The result of the INAV receiving the attack coordinates at the same time as it is receiving the mission coordinates to be carried out

![Screen missione coordinate Attacco](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Coordinate_attaccante.png)

## RC command terminal

After completing the gps attack , we go to the radio command terminal and run this script to initiate commands to direct the drone

```
1. python3 RCmission.py −−ip 172.18.0.2 −−port 5762

```

The result is that INAV receives the commands and shown in the figure below
![Screen coordinate radiocomando MSP](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/rcMission_panel.png)

## Attacker terminal for gps attack

Move to the attacker terminal and launch this command to complete the attack

```
1. python3 AttackRC_msp_fisso.py --ip 172.18.0.2 --port 5761

```

The result of the INAV receiving the attack coordinates at the same time as it is receiving the mission coordinates to be carried out

![Screen comandi di Attacco](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/rc_attack.png)

## 2. Physical Attack

After carrying out a software attack, to see if it was possible to carry out the same attack on a physical level, we equipped ourselves with a dji drone and a HackRF One

## Setting up the Environment

### Physical Instruments

The physical instruments useful for the complete set are a HackRF and a dji drone in this case a Mavic mini 2

![Mavic mini 2](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/mavicmini2-removeb.png)
![HackRF ONE](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/HACKRFOneF.png)

### Software Istruments

The relevant software tool to carry out the attack is gps-sdr-sim available at the following link :https://github.com/osqzss/gps-sdr-sim

```
1. The first step is to download the RINEX navigation files for GPS ephemerides.
It is necessary to download the latest file directly from the NASA website: https://cddis.nasa.gov/archive/gnss/data/daily/.

```

![Rinix1](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Rinix1.png)
![Rinix2](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Rinix2.png)
![Rinix3](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Rinix3.png)
![Rinix4](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Rinix4.png)
![Rinix5](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Rinix5.png)

After downloading the file, copy it into the gps-sdr-sim directory (which has been previously compiled and set according to the guide in the previous link) and run the following command to create the .C8 file for the coordinates

```
 ./gps-sdr-sim -e brdc3170.23n -s 2600000 -b 8 -o TestCina.C8 -l 30.293650, 120.161420,100 -d 10

```

After creating the file, you need to install the hrfs software by following the following linkk guide :https://hackrf.readthedocs.io/en/latest/installing_hackrf_software.html

When installation is complete, connect the whole set as in the photo:

![setComplite](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/set_complite.png)

Now, after connecting everything, you need to move to the gps-sdr-sim directory and run the following command to start the attack

```
 ./hackrf_transfer -t Testcina.C8 -f 1575420000 -s 2600000 -a 0

```

Running scripts

![Running scripts](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/runnung_script.png)

### Results

![Risultato1](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Risultato1.png)

![Risultato2](https://github.com/NS-unina/GCAP_Mod/blob/main/INAV_Flight_controller/Screen_attacco/Risultato2.jpg)
