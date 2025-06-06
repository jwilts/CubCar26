# Rotary_Test.py
# Pin 17 - DT - GP13
# Pin 19 - CLK - GP14
# Pin 20 - SW - GP15
# Pin 38 - GND
# Pin 36 - PWR

import time  
from rotary_irq_rp2 import RotaryIRQ  
from machine import Pin  
SW=Pin(15,Pin.IN,Pin.PULL_UP)  
r = RotaryIRQ(pin_num_clk=14,   
    pin_num_dt=13,
    min_val=0,
    reverse=True,
    range_mode=RotaryIRQ.RANGE_UNBOUNDED)  
val_old = r.value()  
while True:  
    try:  
        val_new = r.value()  
        if SW.value()==0 and n==0:  
            print("Button Pressed")  
            print("Selected Number is : ",val_new)  
            n=1  
            while SW.value()==0:  
             continue  
        n=0  
        if val_old != val_new:  
           val_old = val_new  
           print('result =', val_new)  
        time.sleep_ms(50)  
    except KeyboardInterrupt:  
        break  