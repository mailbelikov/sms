import serial

try:
    ser = serial.Serial('COM4',9600)
    print(ser.name, ' port connected')
    ser.close()

except serial.SerialException:
    print('Port error')

