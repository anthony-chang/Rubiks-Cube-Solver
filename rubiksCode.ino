#include <Stepper.h>
// Define number of steps per rotation as 2048
const int stepsPerRevolution = 2048;
 
Stepper front = Stepper(stepsPerRevolution, 2, 4, 3, 5); //connected in1 -> 1, in2 -> 2, 3, 4..., + -> 5v, - -> gnd
Stepper right = Stepper(stepsPerRevolution, 6, 7, 6, 8);
Stepper upper = Stepper(stepsPerRevolution, 9,11,10,12);
Stepper left = Stepper(stepsPerRevolution, 13, 15, 14, 16);
Stepper back = Stepper(stepsPerRevolution, 17,19,18,20);
Stepper down = Stepper(stepsPerRevolution, 21,23,22,24);

//reading the input from serial and creating char array
int inputting(char* buffer){
  int len = 0;
  while(Serial.available()) {
    delay(100);
    buffer[len++] = Serial.read();
  }
  return len;
}


void setup() {
  // Set the speed to 15 rpm:
  front.setSpeed(15);
  right.setSpeed(15);
  upper.setSpeed(15);
  left.setSpeed(15);
  back.setSpeed(15);
  down.setSpeed(15);
 // Begin Serial communication at a baud rate of 9600:
  Serial.begin(38400);
}

//motor actions
#define command(letter, motor)  case letter: \
    switch(ch[i+1]){ \
      case '\'': \
        motor.step(stepsPerRevolution/4); \
        Serial.print("1");\
        ++i; \
        break; \
      case '2': \
        motor.step(stepsPerRevolution/2); \
        Serial.print("2");\
       ++i; \
        break; \
      case ' ': \
      case '\0': \
        motor.step(-stepsPerRevolution/4); \
        Serial.print("3");\
        break; \
     default: \
      break; \
    } \
    break;

void loop() {
  char ch[200];
  memset(ch, 0, sizeof ch);
  int len = inputting(ch);

  for(int i = 0; i < len; i++){
  switch (ch[i]){
  command('F', front)
  command('R', right)
  command('U', upper)
  command('L', left)
  command('B', back)
  command('D', down)
  
  default:
    break;
  }
}

}
