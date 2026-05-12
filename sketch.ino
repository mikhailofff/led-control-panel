#include <SPI.h>

const int ledPins[] = {2, 3, 5, 6, 9};
const int numLeds = 5;

volatile byte spiByte = 0;
volatile bool newCommand = false;

enum Mode { STOP, FORWARD, BACKWARD };
Mode currentMode = STOP;
unsigned long lastAnimTime = 0;
int animStep = 0;
unsigned int animDelay = 150;

void setup() {
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPI.attachInterrupt();
}

ISR(SPI_STC_vect) {
  spiByte = SPDR;
  newCommand = true;
  SPDR = 0xAA;
}

void handleCommand(byte cmd) {
  if (cmd == 0x00) {
    currentMode = STOP;
    for(int i=0; i<numLeds; i++) digitalWrite(ledPins[i], LOW);
  }

  else if (cmd == 0x01) digitalWrite(3, HIGH);
  else if (cmd == 0x02) digitalWrite(3, LOW);
  else if (cmd == 0x03) digitalWrite(5, HIGH);
  else if (cmd == 0x04) digitalWrite(5, LOW);
  else if (cmd == 0x05) digitalWrite(6, HIGH);
  else if (cmd == 0x06) digitalWrite(6, LOW);
  else if (cmd == 0x07) digitalWrite(9, HIGH);
  else if (cmd == 0x08) digitalWrite(9, LOW);
  else if (cmd == 0x09) digitalWrite(2, HIGH);
  else if (cmd == 0x0A) digitalWrite(2, LOW);

  else if (cmd == 0x11) { currentMode = FORWARD; animStep = 0; }
  else if (cmd == 0x12) { currentMode = BACKWARD; animStep = numLeds - 1; }
  else if (cmd >= 5 && cmd <= 50) {
    animDelay = cmd * 10;
  }
}

void loop() {
  if (newCommand) {
    newCommand = false;
    handleCommand(spiByte);
  }

  if (currentMode != STOP) {
    if (millis() - lastAnimTime >= animDelay) {
      lastAnimTime = millis();

      for(int i=0; i<numLeds; i++) digitalWrite(ledPins[i], LOW);

      digitalWrite(ledPins[animStep], HIGH);

      if (currentMode == FORWARD) {
        animStep++;
        if (animStep >= numLeds) animStep = 0;
      } else {
        animStep--;
        if (animStep < 0) animStep = numLeds - 1;
      }
    }
  }
}
