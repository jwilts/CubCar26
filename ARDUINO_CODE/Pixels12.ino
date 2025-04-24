// #########################################################################################################
// LED Control System for Arduino
// This program interfaces with a Python script to receive LED control commands via serial communication.
// It supports a variety of LED effects and LCD messages. Commands are sent from Python in the following format:
//    "LED|<led_number>|<bank>|<place>|<effect>|<brightness>|<color>\n"
//    "DISPLAY_LCD|<row>|<message>\n" or "CLEAR_LCD\n"
// After processing a command, the Arduino sends back an "<ACK>" to confirm reception and processing.
// #########################################################################################################

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <FastLED.h>

// LCD setup
LiquidCrystal_I2C lcd(0x27, 20, 4); // 20x4 I2C LCD display

// LED setup
#define NUM_LEDS 12   // Number of LEDs in the first LED strip (Tracklights)
#define NUM_LEDS2 9   // Number of LEDs in the second LED strip (WinnerLights)
#define NUM_LEDS3 3   // Number of LEDs in the third LED strip
#define DATA_PIN1 6   // Pin for the first LED strip
#define DATA_PIN2 7   // Pin for the second LED strip
#define DATA_PIN3 8   // Pin for the third LED strip
#define LaneCount 3   // Number of lanes per bank

// Define LED arrays for each strip
CRGB leds1[NUM_LEDS];
CRGB leds2[NUM_LEDS2];
CRGB leds3[NUM_LEDS3];

// Define effects
enum Effect { OFF, BREATHING, CHASER, RAINBOW, BLINK, CONFETTI, SINELON, BPM, JUGGLE, LIGHT_UP_BANK, LIGHT_PLACE, FULL, FLASH };
Effect currentEffect1 = OFF; // Current effect for the first LED strip
Effect currentEffect2 = OFF; // Current effect for the second LED strip
Effect currentEffect3 = OFF; // Current effect for the third LED strip

// Brightness levels for each strip
uint8_t brightness1 = 50;
uint8_t brightness2 = 50;
uint8_t brightness3 = 50;

// Bank and place tracking for each strip
int currentBank1 = 0;
int currentBank2 = 0;
int currentBank3 = 0;
int currentPlace1 = 0;
int currentPlace2 = 0;
int currentPlace3 = 0;

// Base colors for each strip
CRGB baseColor1 = CRGB::White;
CRGB baseColor2 = CRGB::White;
CRGB baseColor3 = CRGB::White;

uint8_t gHue = 0;  // Controls the global hue for color effects
bool serialReceived = false; // Flag to indicate if serial data has been received

// Function prototypes
void parseCommand(String command);
Effect getEffectByName(String name);
CRGB getColorByName(String colorName);
void applyEffect(Effect effect, CRGB* leds, int numLeds, int bank, int place, CRGB baseColor);
void applyFullEffect(CRGB* leds, int numLeds, CRGB color, uint8_t brightness);
void applyFlashEffect(CRGB* leds, int numLeds, CRGB color);
void applyBreathingEffect(CRGB* leds, int numLeds);
void applyChaserEffect(CRGB* leds, int numLeds);
void lightUpBank(CRGB* leds, int numLeds, int bank, CRGB baseColor);
void lightPlace(CRGB* leds, int numLeds, int bank, int place, CRGB color);
void applyBlinkEffect(CRGB* leds, int numLeds);
void confettiEffect(CRGB* leds, int start, int count, unsigned long currentMillis);
void sinelonEffect(CRGB* leds, int start, int count, unsigned long currentMillis);
void bpmEffect(CRGB* leds, int start, int count, unsigned long currentMillis);
void juggleEffect(CRGB* leds, int start, int count, unsigned long currentMillis);

void setup() {
  // Initialize the LCD
  lcd.init();
  lcd.backlight();
  Serial.begin(57600);

  // Display initial message on the LCD
  lcd.setCursor(0, 0);
  lcd.print("Receiving Data");
  lcd.setCursor(0, 1);
  lcd.print("Please wait...");

  // Add LED strips to FastLED
  FastLED.addLeds<WS2812, DATA_PIN1, GRB>(leds1, NUM_LEDS);   // First strip
  FastLED.addLeds<WS2812, DATA_PIN2, RGB>(leds2, NUM_LEDS2);    // Second strip
  FastLED.addLeds<WS2812, DATA_PIN3, RGB>(leds3, NUM_LEDS3);    // Third strip

  // Set initial brightness
  FastLED.setBrightness(brightness1);
}

// Main program loop
void loop() {
  // Handle default behavior before serial data is received
  if (!serialReceived) {
    static unsigned long lastFlashTime = 0;
    static bool flashState = false;
    /*
    // Light up the first strip in white
    fill_solid(leds1, NUM_LEDS, CRGB::White);
    FastLED.setBrightness(255);
    FastLED.show();

    // Flash the first LED on the second strip
    if (millis() - lastFlashTime >= 500) {
      lastFlashTime = millis();
      flashState = !flashState;
      leds2[0] = flashState ? CRGB::White : CRGB::Black;
      for (int i = 1; i < NUM_LEDS2; i++) leds2[i] = CRGB::Black;
      FastLED.show();
    }

    // Flash the first LED on the third strip
    if (millis() - lastFlashTime >= 500) {
      lastFlashTime = millis();
      flashState = !flashState;
      leds3[0] = flashState ? CRGB::White : CRGB::Black;
      for (int i = 1; i < NUM_LEDS3; i++) leds3[i] = CRGB::Black;
      FastLED.show();
    }
    */ 

    // Check for serial data
    if (Serial.available()) {
      serialReceived = true;
      fill_solid(leds1, NUM_LEDS, CRGB::Black); // Turn off the first strip
      FastLED.show();
    }
    return;
  }

  // Increment hue for color effects
  EVERY_N_MILLISECONDS(20) { gHue++; }

  // Parse serial commands
  while (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    parseCommand(command);
    // Send acknowledgment back to the sender
++    Serial.println("<ACK>");
  }

  // Apply effects to each LED strip
  applyEffect(currentEffect1, leds1, NUM_LEDS, currentBank1, currentPlace1, baseColor1);
  applyEffect(currentEffect2, leds2, NUM_LEDS2, currentBank2, currentPlace2, baseColor2);
  applyEffect(currentEffect3, leds3, NUM_LEDS3, currentBank3, currentPlace3, baseColor3);

  // Update LEDs
  FastLED.show();
} // End main loop

// Parse incoming serial command and update LED strip states
void parseCommand(String command) {
  if (command.startsWith("LED")) {
    // Extract command parameters
    int firstSep = command.indexOf('|', 4);
    int secondSep = command.indexOf('|', firstSep + 1);
    int thirdSep = command.indexOf('|', secondSep + 1);
    int fourthSep = command.indexOf('|', thirdSep + 1);
    int fifthSep = command.indexOf('|', fourthSep + 1);
    int sixthSep = command.indexOf('|', fifthSep + 1);

    int ledStrip = command.substring(4, firstSep).toInt();
    int bank = command.substring(firstSep + 1, secondSep).toInt();
    int place = command.substring(secondSep + 1, thirdSep).toInt();
    String effect = command.substring(thirdSep + 1, fourthSep);
    int brightness = command.substring(fourthSep + 1, fifthSep).toInt();
    String colorName = command.substring(fifthSep + 1, sixthSep);

    // Get base color from the color name
    CRGB baseColor = getColorByName(colorName);

    // Update the appropriate LED strip
    if (ledStrip == 1) {
      currentEffect1 = getEffectByName(effect);
      brightness1 = brightness;
      currentBank1 = bank;
      currentPlace1 = place;
      baseColor1 = baseColor;
    } else if (ledStrip == 2) {
      currentEffect2 = getEffectByName(effect);
      brightness2 = brightness;
      currentBank2 = bank;
      currentPlace2 = place;
      baseColor2 = baseColor;
    } else if (ledStrip == 3) {
      currentEffect3 = getEffectByName(effect);
      brightness3 = brightness;
      currentBank3 = bank;
      currentPlace3 = place;
      baseColor3 = baseColor;
    }
  } else if (command.startsWith("CLEAR_LCD")) {
    lcd.clear(); // Clear the LCD
  } else if (command.startsWith("DISPLAY_LCD")) {
    // Display a message on the LCD
    int firstSep = command.indexOf('|');
    int row = command.substring(firstSep + 1).toInt();
    String message = command.substring(firstSep + 3);
    lcd.setCursor(0, row);
    lcd.print(message);
  }
} // End parseCommand

// GetEffectByName
Effect getEffectByName(String name) {
  if (name == "BREATHING") return BREATHING;
  if (name == "CHASER") return CHASER;
  if (name == "RAINBOW") return RAINBOW;
  if (name == "BLINK") return BLINK;
  if (name == "CONFETTI") return CONFETTI;
  if (name == "SINELON") return SINELON;
  if (name == "BPM") return BPM;
  if (name == "JUGGLE") return JUGGLE;
  if (name == "LIGHT_UP_BANK") return LIGHT_UP_BANK;
  if (name == "LIGHT_PLACE") return LIGHT_PLACE;
  if (name == "FULL") return FULL;
  if (name == "FLASH") return FLASH;
  return OFF;
} // End getEffectByName

// Get ColorByName
CRGB getColorByName(String colorName) {
  if (colorName == "RED") return CRGB::Red;
  if (colorName == "GREEN") return CRGB::Green;
  if (colorName == "BLUE") return CRGB::Blue;
  if (colorName == "WHITE") return CRGB::White;
  if (colorName == "YELLOW") return CRGB::Yellow;
  if (colorName == "CYAN") return CRGB::Cyan;
  if (colorName == "MAGENTA") return CRGB::Magenta;
  return CRGB::Black;
} // End getColorByName

// applyEffect
void applyEffect(Effect effect, CRGB* leds, int numLeds, int bank, int place, CRGB baseColor) {
  switch (effect) {
    case BREATHING:
      applyBreathingEffect(leds, numLeds);
      break;
    case CHASER:
      applyChaserEffect(leds, numLeds);
      break;
    case RAINBOW:
      fill_rainbow(leds, numLeds, millis() / 256);
      break;
    case BLINK:
      applyBlinkEffect(leds, numLeds);
      break;
    case CONFETTI:
      confettiEffect(leds, 0, numLeds, millis());
      break;
    case SINELON:
      sinelonEffect(leds, 0, numLeds, millis());
      break;
    case BPM:
      bpmEffect(leds, 0, numLeds, millis());
      break;
    case JUGGLE:
      juggleEffect(leds, 0, numLeds, millis());
      break;
    case LIGHT_UP_BANK:
      lightUpBank(leds, numLeds, bank, baseColor);
      break;
    case LIGHT_PLACE:
      lightPlace(leds, numLeds, bank, place, baseColor);
      break;
    case FULL:
      applyFullEffect(leds, numLeds, baseColor, brightness1);
      break;
    case FLASH:
      applyFlashEffect(leds, numLeds, baseColor);
      break;
    case OFF:
      fill_solid(leds, numLeds, CRGB::Black);
      break;
  }
} // End applyEffect

// applyFullEffect (Light whole Strip)
void applyFullEffect(CRGB* leds, int numLeds, CRGB color, uint8_t brightness) {
  FastLED.setBrightness(brightness);
  fill_solid(leds, numLeds, color);
  FastLED.show();
} // End applyFullEffect

// applyFlashEffect (Flash twice)
void applyFlashEffect(CRGB* leds, int numLeds, CRGB color) {
  for (int i = 0; i < 2; i++) {
    fill_solid(leds, numLeds, color);
    FastLED.show();
    delay(100);
    fill_solid(leds, numLeds, CRGB::Black);
    FastLED.show();
    delay(100);
  }
} // End applyFlashEffect

void applyBreathingEffect(CRGB* leds, int numLeds) {
  float phase = (millis() % 4000) / 4000.0;
  uint8_t brightness = (exp(sin(phase * PI)) - 0.36787944) * 108.0;
  for (int i = 0; i < numLeds; i++) leds[i] = CHSV(gHue, 255, brightness);
} // End applyBreathingEffect

void applyChaserEffect(CRGB* leds, int numLeds) {
  static int pos = 0;
  EVERY_N_MILLISECONDS(50) {
    fill_solid(leds, numLeds, CRGB::Black);
    leds[pos] = CHSV(gHue, 255, 255);
    pos = (pos + 1) % numLeds;
  }
} // End applyChaserEffect

void lightUpBank(CRGB* leds, int numLeds, int bank, CRGB baseColor) {
  int startLed = (bank - 1) * LaneCount;
  int endLed = startLed + LaneCount;
  if (endLed > numLeds) endLed = numLeds;

  for (int i = startLed; i < endLed; i++) {
    leds[i] = baseColor; // Light up specified LEDs in the bank
  }
} // End lightUpBank

void lightPlace(CRGB* leds, int numLeds, int bank, int place, CRGB color) {
  // Determine the start and end indices for the specified bank.
  int startLed = (bank - 1) * LaneCount;
  int endLed = startLed + LaneCount;
  if (endLed > numLeds) {
    endLed = numLeds;
  }
  
  // Calculate the index up to which the LEDs should be lit.
  // (Note: place is assumed to be 1-indexed; place = 3 lights LEDs at indices startLed, startLed+1, and startLed+2)
  int lightEnd = startLed + place;
  if (lightEnd > endLed) {
    lightEnd = endLed;
  }
  
  // Iterate through all LEDs in the bank.
  for (int i = startLed; i < endLed; i++) {
    if (i < lightEnd) {
      leds[i] = color;      // Light this LED with the specified color.
    } else {
      leds[i] = CRGB::Black;  // Turn off the remaining LEDs.
    }
  }
}

void applyBlinkEffect(CRGB* leds, int numLeds) {
  static bool on = false;
  on = !on;
  fill_solid(leds, numLeds, on ? CRGB(CHSV(gHue, 255, 255)) : CRGB::Black);
} // End applyBlinkEffect

void confettiEffect(CRGB* leds, int start, int count, unsigned long currentMillis) {
  fadeToBlackBy(leds + start, count, 10);
  int pos = random16(count);
  leds[start + pos] += CHSV(gHue + random8(64), 200, 255);
} // End confettiEffect

void sinelonEffect(CRGB* leds, int start, int count, unsigned long currentMillis) {
  fadeToBlackBy(leds + start, count, 20);
  int pos = beatsin16(13, 0, count - 1);
  leds[start + pos] += CHSV(gHue, 255, 192);
} // End sinelonEffect

void bpmEffect(CRGB* leds, int start, int count, unsigned long currentMillis) {
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8(BeatsPerMinute, 64, 255);
  for (int i = 0; i < count; i++) {
    leds[start + i] = ColorFromPalette(palette, gHue + (i * 2), beat - gHue + (i * 10));
  }
} // End bpmEffect

void juggleEffect(CRGB* leds, int start, int count, unsigned long currentMillis) {
  fadeToBlackBy(leds + start, count, 20);
  uint8_t dothue = 0;
  for (int i = 0; i < 8; i++) {
    leds[start + beatsin16(i + 7, 0, count - 1)] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
} // End juggleEffect

