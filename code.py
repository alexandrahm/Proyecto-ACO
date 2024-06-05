#include <Adafruit_LiquidCrystal.h> 
#define NOTE_C4 262

int luz = 0;
int gas = 0;
int distance = 0;
int motor = 10;
int foco = 11;
int sensor_luz = 12; //conectado a pin 12
const int trigPin = 6;
const int echoPin = 5;
long duration;
int tiltPin = 3; // Pin digital donde está conectado el sensor de inclinación
int tiltState = 0; // Variable para almacenar el estado del sensor de inclinación

Adafruit_LiquidCrystal lcd_1(0);//inicializando lcd

void setup() {
  lcd_1.begin(16, 2);
  lcd_1.print("Luz: Gas: Obj: ");

  pinMode(sensor_luz, INPUT);//modo entrada para el pin
  pinMode(foco, OUTPUT);//mandar cuanta energia debe dejar pasar el transistor para encender foco
  pinMode(motor, OUTPUT);
  pinMode(trigPin, OUTPUT);//tipo salida para distancia
  pinMode(echoPin, INPUT);
  pinMode(tiltPin, INPUT_PULLUP); // Configurar el pin del sensor de inclinación como entrada con resistencia pull-up interna

  Serial.begin(9600); // Inicializar comunicación serie
}

void loop() {
  //Para el sensor de luz
  luz = digitalRead(sensor_luz);//saber si hay o no luz
  digitalWrite(foco, luz == 0 ? HIGH : LOW); //cuando no haya luz se enciende el foco
  
  //Para sensor de gas
  gas = analogRead(A0);
  gas = map(gas, 300, 750, 0, 100);//función que llama a otra
  digitalWrite(motor, gas >= 50 ? HIGH : LOW); //hay gas sí o no?
  if (gas >= 50) {//se usa piezo como alarma, si el usuario esta en peligro sonará
    tone(8, NOTE_C4, 250);//(tono 8, frecuencia y tiempo en milisegundos)
  }
  
  //para sensor de inclinacion
  tiltState = digitalRead(tiltPin); // Leer el estado del sensor de inclinación
  if (tiltState == LOW) { // Si el sensor de inclinación está activado (asumiendo que se cierra el circuito cuando se inclina)
    Serial.println("Inclinación detectada!"); // Imprimir mensaje
  } else {
    Serial.println("No hay inclinación"); // Imprimir mensaje
  }
  
  //Para sensor ultrasónico y medir distancia
  digitalWrite(trigPin, LOW);// inicializando apagado
  delayMicroseconds(2);//microsegundos
  digitalWrite(trigPin, HIGH);//dispara sonido 10 microsegundos
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);//apagando
  duration = pulseIn(echoPin, HIGH);//medir duración
  distance = int(duration * 0.034 / 2);//medir distancia con respecto a la duración
  if (distance <= 5) {//detectar objeto cerca a 5 cm de distancia
    tone(8, NOTE_C4, duration);//(tono 8, frecuencia y tiempo en milisegundos)
  }
  
  //A mostrar en pantalla lcd
  lcd_1.setCursor(0, 1);//columna 0, fila 1
  lcd_1.print(luz);
  lcd_1.setCursor(5, 1);
  lcd_1.print(gas);
  lcd_1.setCursor(10, 1);
  lcd_1.print(distance);
  
  // Mostrar estado del sensor de inclinación en la pantalla LCD
  lcd_1.setCursor(0, 0); // Columna 0, fila 0
  lcd_1.print("Tilt: ");
  if (tiltState == LOW) {
    lcd_1.print("YES ");
  } else {
    lcd_1.print("NO  ");
  }

  //Refrescando pantalla lcd
  lcd_1.setBacklight(1);//blink
  delay(500);//milisegundo
  lcd_1.setBacklight(0);
  delay(500);
}
