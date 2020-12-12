#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

int minimumRange=65;
int maximumRange=75;
int readcount=0;

float stemp=0;
float roomTemp=0;
float distance =0;
float objectTemp =0;
float finaltemp =0;
float threshold  =22;// for calibration

long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  return pulseIn(echoPin, HIGH);
}

void setup()
{
  Serial.begin(9600);
  //Serial.println("Temperature");  
  mlx.begin();
  pinMode(6, OUTPUT); //red led
  pinMode(7, OUTPUT); //green led
  pinMode(8, OUTPUT); //yellow led
}

void loop()
{
  distance = 0.01723 * readUltrasonicDistance(12, 11);
 // Serial.print("distance-");
 // Serial.print(distance);
 // Serial.println("cm");
  delay(100);
  
  //Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC());
  //Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");
  //Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempF());
  //Serial.print("*F\tObject = "); Serial.print(mlx.readObjectTempF()); Serial.println("*F");
  //Serial.println();
  //delay(100);
  
  // reading object and ambient  temperature
  objectTemp = threshold + mlx.readObjectTempF() ;
  roomTemp = mlx.readAmbientTempF() ;
   
  if (distance > maximumRange) 
  {
    //Serial.println("GET CLOSER");
    get_closer();
  }
 
  if (distance < minimumRange) 
  {
    //Serial.println("TOO CLOSE!");
    too_close();
  }
  if ((distance >= minimumRange) && (distance <= maximumRange))
  {
    if (readcount == 1) 
    {  // after reading 1 time
      displaytemp();
    } 
    else 
    {
      //Serial.println("HOLD ON");// when in range, ask user to hold position
      hold_on();
      stemp = stemp + objectTemp;
      readcount++;
      delay(200);      // until approx 200 ms
    }
  } 
  else 
  {     // if user is out of range, reset calculation
    delay(100);
    readcount = 0;
    stemp = 0;
  }
  delay(100);
}
void displaytemp()
{
  finaltemp = stemp / 1;       // get the reading of temp
  //Serial.println("YOUR TEMP:");
  Serial.println(String(finaltemp)+ "F");
  readcount = 0;
  stemp = 0;
  if (objectTemp >= 99) 
  {
    play_alert();
  } 
  else 
  {
    play_ok();
  }
delay(500); 
}
void play_ok() {  // play one note when object temperature is below 37.5C
  tone(3, 600, 1000);  // pin,frequency,duration
  delay(200);
  tone(3, 750, 500);
  delay(100);
  tone(3, 1000, 500);
  delay(200);
  //noTone(3);
}

void play_alert() { // beep 3x when object temperature is >= 37.5C
  tone(3, 2000, 1000);
  delay(1000);
  tone(3, 3000, 1000);
  delay(1000);
  tone(3, 4000, 1000);
  delay(1000);
  noTone(3);
}
void hold_on()
{
  digitalWrite(7, HIGH);
  digitalWrite(8, LOW);
  digitalWrite(6, LOW);
}
void get_closer()
{
  digitalWrite(8, HIGH);
  digitalWrite(7, LOW);
  digitalWrite(6, LOW);
 }
 void too_close()
{
  digitalWrite(6, HIGH); 
  digitalWrite(8, LOW);
  digitalWrite(7, LOW);
 }
