#include <Stepper.h>
// Define number of steps per rotation as 2048
const int stepsPerRevolution = 2048;
const int SPEED = 13;
 
Stepper front = Stepper(stepsPerRevolution, 2, 4, 3, 5); //connected in1 -> 1, in2 -> 2, 3, 4..., + -> 5v, - -> gnd
Stepper right = Stepper(stepsPerRevolution, 6, 8, 7, 9);
Stepper upper = Stepper(stepsPerRevolution, 10,12,11,13);
Stepper left = Stepper(stepsPerRevolution, 22,24,23,25);
Stepper back = Stepper(stepsPerRevolution, 26,28,27,29);
Stepper down = Stepper(stepsPerRevolution, 38,40,39,41);

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
  front.setSpeed(SPEED);
  right.setSpeed(SPEED);
  upper.setSpeed(SPEED);
  left.setSpeed(SPEED);
  back.setSpeed(SPEED);
  down.setSpeed(SPEED);
 // Begin Serial communication at a baud rate of 38400:
  Serial.begin(38400);
}

//motor actions
#define command(letter, motor)  case letter: \
    switch(ch[i+1]){ \
      case '\'': \
        motor.step(stepsPerRevolution/4); \
        ++i; \
        break; \
      case '2': \
        motor.step(stepsPerRevolution/2); \
       ++i; \
        break; \
      case ' ': \
      case '\0': \
        motor.step(-stepsPerRevolution/4); \
        break; \
     default: \
      break; \
    } \
    break;

void loop() {
  char ch[400];
  memset(ch, 0, sizeof ch);
  int len = inputting(ch);
  for(int i = 0; i < len; i++){
    Serial.print(ch[i]+ ch[i+1] + " ");
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
