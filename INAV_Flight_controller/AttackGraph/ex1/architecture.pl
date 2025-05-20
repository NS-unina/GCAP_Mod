/* Attack goal */
attackGoal(canSpoof(feedbackFlow4)).

/* Attacker location */
attackerLocated(coverZone).

/* Control flow satellite to GPS Module */
controlFlow(satellite, gpsModule, feedbackFlow4).
physicalLayer(nmea0183, gpsModule, satellite).
weaknessPhysicalLayer(ac7, nmea0183, coverZone).

