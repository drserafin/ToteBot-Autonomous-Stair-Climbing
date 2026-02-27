import sys
import ArducamDepthCamera as ac

cam = ac.ArducamCamera()
if cam.open(ac.Connection.CSI, 0) != 0:
    print("Camera failed to open")
    sys.exit()

cam.start(ac.FrameType.DEPTH)

# Grab exactly one frame
frame = cam.requestFrame(2000)

print("\n--- NEW FRAME ATTRIBUTES ---")
# dir() asks Python to list every command this object accepts
print(dir(frame)) 
print("----------------------------\n")

cam.releaseFrame(frame)
cam.stop()
cam.close()
