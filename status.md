Status

Version 1.0
Copied everything from avcourt/restful-pi 
runs fine
Able to control all LEDs via swagger and Postman.
HINT: on POSTMAN you need change Settings: Body: RAW: JSON
if you want to do a PUT or POST


Version 1.1
Added byte_model and ByteOutputUtil
wrote the get function. 
I am now able to make a get on /byte and the right 8bit Int value is delivered.

Version 1.2
Added update to ByteOutputUtil
It is now possible to do a put on /byte. 
It works, but the problem is that the information on LED data is now corrupt.
I have to refactor the code and think of how the data should be kept.