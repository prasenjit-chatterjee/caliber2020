import smbus
import time


class lcd_i2c:
    # Define some device parameters
    I2C_ADDR = 0x27  # I2C device address
    LCD_WIDTH = 16   # Maximum characters per line

    # Define some device constants
    LCD_CHR = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

    LCD_BACKLIGHT = 0x08  # On
    # LCD_BACKLIGHT = 0x00  # Off

    ENABLE = 0b00000100  # Enable bit

    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    # Open I2C interface
    # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1    

    def lcd_init(self):
        # Initialise display
        lcd_i2c.lcd_byte(self, 0x33, lcd_i2c.LCD_CMD)  # 110011 Initialise
        lcd_i2c.lcd_byte(self, 0x32, lcd_i2c.LCD_CMD)  # 110010 Initialise
        lcd_i2c.lcd_byte(self, 0x06, lcd_i2c.LCD_CMD)  # 000110 Cursor move direction
        lcd_i2c.lcd_byte(self, 0x0C, lcd_i2c.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        # 101000 Data length, number of lines, font size
        lcd_i2c.lcd_byte(self, 0x28, lcd_i2c.LCD_CMD)
        lcd_i2c.lcd_byte(self, 0x01, lcd_i2c.LCD_CMD)  # 000001 Clear display
        time.sleep(lcd_i2c.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | lcd_i2c.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | lcd_i2c.LCD_BACKLIGHT

        # High bits
        lcd_i2c.bus.write_byte(lcd_i2c.I2C_ADDR, bits_high)
        lcd_i2c.lcd_toggle_enable(self, bits_high)

        # Low bits
        lcd_i2c.bus.write_byte(lcd_i2c.I2C_ADDR, bits_low)
        lcd_i2c.lcd_toggle_enable(self, bits_low)

    def lcd_toggle_enable(self,bits):
        # Toggle enable
        time.sleep(lcd_i2c.E_DELAY)
        lcd_i2c.bus.write_byte(lcd_i2c.I2C_ADDR, (bits | lcd_i2c.ENABLE))
        time.sleep(lcd_i2c.E_PULSE)
        lcd_i2c.bus.write_byte(lcd_i2c.I2C_ADDR, (bits & ~lcd_i2c.ENABLE))
        time.sleep(lcd_i2c.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(lcd_i2c.LCD_WIDTH, " ")
        lcd_i2c.lcd_byte(self, line, lcd_i2c.LCD_CMD)
        for i in range(lcd_i2c.LCD_WIDTH):
            lcd_i2c.lcd_byte(self, ord(message[i]), lcd_i2c.LCD_CHR)

    def __init__(self):
        lcd_i2c.lcd_init(self)

    def right_to_left_scroll(self, text, row_no):
          str_pad = " " * 16
          scroll_text = str_pad + text
          for i in range (0, len(scroll_text)):
                if row_no == 1 :                      
                  lcd_i2c.lcd_string(self, scroll_text[i:(i+16)], lcd_i2c.LCD_LINE_1)
                  time.sleep(0.15)
                  lcd_i2c.lcd_string(self, str_pad, lcd_i2c.LCD_LINE_1)
                elif row_no == 2:
                    lcd_i2c.lcd_string(self, scroll_text[i:(i+16)], lcd_i2c.LCD_LINE_2)
                    time.sleep(0.15)
                    lcd_i2c.lcd_string(self, str_pad, lcd_i2c.LCD_LINE_2)
                elif row_no == 100:
                    lcd_i2c.lcd_string(self, scroll_text[i:(i+16)], lcd_i2c.LCD_LINE_1)
                    time.sleep(0.11)
                    lcd_i2c.lcd_string(self, str_pad, lcd_i2c.LCD_LINE_1)
                    
                    lcd_i2c.lcd_string(self, scroll_text[i:(i+16)], lcd_i2c.LCD_LINE_2)
                    time.sleep(0.11)
                    lcd_i2c.lcd_string(self, str_pad, lcd_i2c.LCD_LINE_2)
