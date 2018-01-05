from AirSimClient import *
#from keras.models import load_model
import sys
import numpy as np

#if (len(sys.argv) != 2):
#    print('usage: python drive.py <modelName>')
#    sys.exit()

#print('Loading model...')
#model = load_model(sys.argv[1])

# connect to the AirSim simulator 
client = CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = CarControls()

car_controls.steering = 0
car_controls.throttle = 0
car_controls.brake = 0

image_buf = np.zeros((1, 144, 256, 3))
state_buf = np.zeros((1,4))

def get_image():
    image = client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])[0]
    image1d = np.fromstring(image.image_data_uint8, dtype=np.uint8)
    image_rgba = image1d.reshape(image.height, image.width, 4)
    image_rgba = np.flipud(image_rgba)
    return image_rgba[:, :, 0:3]

while (True):
    car_state = client.getCarState()
   
    print('car speed: {0}'.format(car_state.speed))
    
    if (car_state.speed < 20):
        car_controls.throttle = 1.0
    else:
        car_controls.throttle = 0.0
    
    #image_buf[0] = get_image()
    #state_buf[0] = np.array([car_controls.steering, car_controls.throttle, car_controls.brake, car_state.speed])
    #model_output = model.predict([image_buf, state_buf])
    #car_controls.steering = float(model_output[0][0])
    car_controls.steering = 0
    
    print('Sending steering = {0}, throttle = {1}'.format(car_controls.steering, car_controls.throttle))
    
    client.setCarControls(car_controls)

