# import setup_path
import airsim

import sys
import time

print("""This script is designed to fly on the streets of the Neighborhood environment
and assumes the unreal position of the drone is [160, -1500, 120].""")

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
# client.simEnableWeather(True)
# client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.25)
# client.simSetTimeOfDay(is_enabled, start_datetime = "", is_start_datetime_dst = False, celestial_clock_speed = 1, update_interval_secs = 60, move_sun = True)


print("arming the drone...")
client.armDisarm(True)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync().join()
else:
    client.hoverAsync().join()

time.sleep(3)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("take off failed...")
    sys.exit(1)

# AirSim uses NED coordinates so negative axis is up.
# z of -5 is 5 meters above the original launch point.
z = -3.5
speed = 5 #m/s

print("make sure we are hovering at {} meters...".format(-z))

client.moveToPositionAsync(x=0,y=0,z=-3.25,velocity=0.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=10, duration=1.75).join()
time.sleep(0.1)
client.moveToPositionAsync(x=-1,y=0,z=-3.25,velocity=0.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=-10, duration=3.5).join()
time.sleep(0.1)
client.moveToPositionAsync(x=-1,y=-1,z=-3.25,velocity=0.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=10, duration=1.75).join()
time.sleep(0.1)
client.moveToPositionAsync(x=0,y=0,z=-3.25,velocity=0.5).join()
time.sleep(0.1)
print("Path 1: Done")

client.moveToPositionAsync(x=-1,y=0,z=-3.15,velocity=0.5).join()
time.sleep(0.1)
client.moveToPositionAsync(x=-1,y=-0.5,z=-3.0,velocity=0.5).join()
time.sleep(0.1)
client.moveToPositionAsync(x=-1,y=0.5,z=-3.25,velocity=0.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=-10, duration=1).join()
time.sleep(0.1)
print("Path 2: Done")

client.moveToPositionAsync(x=-2,y=0,z=-3.15,velocity=0.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=10, duration=1.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=-10, duration=3.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=10, duration=4.5).join()
time.sleep(0.1)
client.rotateByYawRateAsync(yaw_rate=-10, duration=1.5).join()
time.sleep(0.1)
print("Path 3: Done")

# client.moveToPositionAsync(x=-1,y=-1,z=-2.55,velocity=0.5).join()
# time.sleep(0.1)
# print(">")
client.moveToPositionAsync(x=-1,y=1.5,z=-2.65,velocity=0.5).join()
time.sleep(0.1)
print(">")
client.moveToPositionAsync(x=-1,y=0,z=-3.75,velocity=0.5).join()
time.sleep(0.1)
print("Path 4: Done")

# client.moveToPositionAsync(x=-1,y=-1,z=-2.75,velocity=0.5).join()
# time.sleep(0.1)
# client.moveToPositionAsync(x=-1.5,y=0.5,z=-3.15,velocity=0.5).join()
# time.sleep(0.1)
# client.moveToPositionAsync(x=-2,y=2.0,z=-3.75,velocity=0.5).join()
# time.sleep(0.1)
# client.moveToPositionAsync(x=-2,y=1.75,z=-3.75,velocity=0.5).join()
# time.sleep(0.1)
client.moveToPositionAsync(x=-1.5,y=-0.5,z=-2.75,velocity=0.5).join()
time.sleep(0.1)
print("Path 5: Done")

# client.moveByVelocityBodyFrameAsync(vx=1,vy=0,vz=0,duration=10).join()
# client.rotateByYawRateAsync(yaw_rate=10, duration=9).join()

# this method is async and we are not waiting for the result since we are passing timeout_sec=0.

print("flying on path...")

path_NH_0=[airsim.Vector3r(-5,0,z),
       airsim.Vector3r(-5,2,z),
       airsim.Vector3r(-5,-2,z)]

# path_NH_0=[airsim.Vector3r(82,0,z),
#        airsim.Vector3r(82,-130,z),
#        airsim.Vector3r(-5,-130,z),
#         airsim.Vector3r(0, 0,z),
#         airsim.Vector3r(82,0,z),
#        airsim.Vector3r(82,-130,z),
#        airsim.Vector3r(-5,-130,z),
#        airsim.Vector3r(0,-20,z)]

# path_NH_1=[airsim.Vector3r(125,0,z)]

# result = client.moveOnPathAsync(path_NH_0, velocity=speed, timeout_sec=600,
#         drivetrain=airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False,0), lookahead=20, adaptive_lookahead=1).join()

# for i in range(len(path_Park)):
#     client.moveToPositionAsync(path_Park[i].x_val,
#                                path_Park[i].y_val,
#                                path_Park[i].z_val, velocity=speed).join()

# drone will over-shoot so we bring it back to the start point before landing.

client.moveToPositionAsync(0,0,0, velocity=5).join()
# client.simSetVehiclePose()
# client.moveByVelocityBodyFrameAsync()
print("landing...")
client.landAsync().join()
print("disarming...")
client.armDisarm(False)
client.enableApiControl(False)
print("done.")