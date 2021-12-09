/*
 * V5 Current
 * 
 */
 
/*
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif
*/


#include <AccelStepper.h>
#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Bool.h>

ros::NodeHandle  nh;


int servoPul = 9;
int driverPul = 6;
int driverDir = 7;
int driverEn = 5;
//int driverAl = 4;  future dev
//int microStpn = 800; //microstepping value


Servo servo;

//servo callback function
void servo_cb( const std_msgs::UInt16& cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
}

ros::Subscriber<std_msgs::UInt16> servo_1("servo", &servo_cb);


AccelStepper stepper_1(1,driverPul,driverDir);

//stepper run callback function
void stepper_run(const std_msgs::Int16& run_truth){
  if(run_truth.data){
    stepper_1.runToNewPosition(run_truth.data);
    stepper_1.setCurrentPosition(0);
    stepper_1.setSpeed(8000);
  }
  }
  
ros::Subscriber<std_msgs::Int16> stepper_rn("stepperRun", &stepper_run);


//stepper enable callback function
void stepper_ena(const std_msgs::Bool& ena_truth){
  if(ena_truth.data){
    digitalWrite(driverEn,LOW);
  }
  else{
      digitalWrite(driverEn,HIGH);    
    }
  }
  
ros::Subscriber<std_msgs::Bool> stepper_en("stepperENA", &stepper_ena);  //direction
  
    
void setup(){
  
  
  //pinMode(13, OUTPUT);    //for blinking lights or physical switches
  //pinMode(12, OUTPUT);
  //pinMode(11, OUTPUT);
  //pinMode(10, OUTPUT);
  pinMode(driverEn, OUTPUT);
  //pinMode(4, INPUT);    //alarm state input future dev
  

  digitalWrite(driverEn, HIGH);

  servo.attach(servoPul); //attach it to pin 9

  //initial values could be faster
  stepper_1.setMaxSpeed(4000);    //set these
  stepper_1.setAcceleration(2000);
  stepper_1.setSpeed(800);
  
  nh.initNode();

  nh.subscribe(servo_1);   
  nh.subscribe(stepper_rn);
  //nh.advertise(stepper_al);  future dev
  nh.subscribe(stepper_en);
   
}

void loop(){
  
  //later dev, add step location info to close loop software side
  //get alarm pin status write to alarm topic (pin4)
  //stepper_al.publish( &alarm ) 
  
   nh.spinOnce();
  
  //delay(1);
  
}
