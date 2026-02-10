# 427 Project 1 - Hardware Abstraction with Adapter Pattern

## System Overview
This system takes the temperature reading from either a digital temperature sensor or an analog temperature sensor, or both, and displays a single syncronized result. 
- This solves the problem that multiple sensors create, as two different results needs to be translated differently, but this system can read both.
- Supported sensors include: ADS1110, DHT11.
- The design uses an adapter pattern to check for inputs from each type of sensor in case one is attached instead of the other. It also can swap to a secondary sensor in the case that one malfunctions.
- The client of the system is whomever receives the synced temperature reading from the adapter pattern.

## UML Diagrams
### Use Case Diagram
![](Diagrams/useCaseDiagram.md)
### Activity Diagram
![](Diagrams/activityDiagram.md)
### Sequence Diagram
![](Diagrams/sequenceDiagram.md)
### Class Diagram
![](Diagrams/classDiagram.md)
### State Diagram
![](Diagrams/stateDiagram.md)

## Robustness Improvement Discussion
In a scenario where a sensor read operation fails, instead of a reported failure with a swap to another available sensor, the system should:
- Retry the read operation up to 3 times,
- Wait a short time between retries, and
- Only report failure if all retries fail.

Discussion:

At first glance, I thought the fix should go inside of main, as that is where we manually manage which sensor to use. However, after further thinking, the `main.py` file should not be aware of the sensor failing and implement retry logic. `main.py`'s only job is to recive data and display it. If we added the retry logic there, it would be a "patch" that covers up the issue, not prevents it.

The logic should be implemented inside of the adapter class, or `adapters.py`. The entire point of the adapter classes is to provide an interface to work with the old code and new code. Fixing the code in the driver level (`dh11_lgpio.py`, `ads1110lgpio.py`) is tempting; however, these files are supposed to be low-level and simple. They connect to the sensors and read the data. The adapter classes are supposed to add reliability to the lower-level code. Retry logic to ensure the readings we get are valid is part of making the old code reliable. I would put it in the `get_temperature()` function inside of `adapters.py` and loop through before we return the temp.

## Reflection
