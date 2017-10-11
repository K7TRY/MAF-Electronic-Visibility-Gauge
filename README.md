# Electronic-Visibility-Gauge
Pilots need to have good visibility to approach and land on a runway or airstrip. Many times they get visibility information by talking to people at the airstrip via HF radio. Estimating visibility can be difficult, and visibility can change rapidly. An automated system that can be calibrated would be a great solution.

Possible hardware to use:
Arduino, Raspberry Pi, Cameras, and/or Lasers. Feel free to use other hardware that is in the hobbyist class. In other words, please do not use professional, expensive hardware.

Experiment Hardware Selection
Using a combination of hardware and software create a device that will signal the range of visibility in a known distance. A known distance is a distance that you can measure independently of your experiment using a yard tape measure, Google maps, or some other means that is not depending on your experimental hardware. This known distance will be different based on the hardware solution you select. Make that selection based on the hardware available, and testing environment you can easily use. Most hardware solutions will return a Boolean value, true or false. If your project can “see” the known distance then it returns a true value.

Not everyone will have a range of a mile to work with, and some sensors cannot reach that far. This is a proof of concept, not a working prototype. For example, most hobbyists have access to lasers that have less than 1 watt of power. Given that power limitation, we are not going to be able to sense the reflection of that laser much more than 50 yards. In that situation I recommend using a highly reflective surface like a street sign as your target. 

If you are using Computer Vision (CV), you can detect a geographic feature in the distance, like a mountain, or a manmade object like a building. Another option would be to detect a sign or QR Code. Making such a large QR Code to test this at a good range is not within the budget of most hobbyists, so if you choose this option, reduce your testing range appropriately. 

MAF only flies during the day, so your device does not need to work at night. So using a light color sensor to detect the color of the sky might be a good option. 

Your device can display the visibility result, true or false, by lighting up an LED, displaying a value on a display, sending a value over the network using a transport like MQTT, or other system that is simple and economical. 
 
Definition Of Done
MAF is looking for a proof of concept that gets the visibility detection correct 9 times out of 10. Please remember that even a failed experiment is useful. Do what you can to be successful, but remember that some hardware and distance combinations may not work.

Please fill out the form below to document your test. A video, and still pictures of your experiment, as well as source code and wiring diagram are all part of a completely documented project.

Electronic Visibility Gauge Results

Detection method: _________________________________________________

Detection Target: _________________________________

Detection range: _____________________________________ miles, feet, meters, or yards.

Out of ten consecutive tests, how many results were within the margin of error? _________________

URL for source code and other documentation: _____________________________________________

 ____________________________________________________________________________________

Who is on your development team? _______________________________________________________

 _____________________________________________________________________________________
