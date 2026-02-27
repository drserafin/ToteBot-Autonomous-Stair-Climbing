import sys
import cv2
import numpy as np
import ArducamDepthCamera as ac

def main():
    # --- SETUP CAMERA ---
    cam = ac.ArducamCamera()
    
    if cam.open(ac.Connection.CSI, 0) != 0:
        print("Camera initialization failed! Check wiring.")
        sys.exit()

    if cam.start(ac.FrameType.DEPTH) != 0:
        print("Camera stream failed to start!")
        sys.exit()

    print("Center Trigger Active. Point at stairs! Press ESC to exit.")

    # --- MAIN LOOP ---
    while True:
        frame = cam.requestFrame(2000)
        if frame is None:
            continue

        # 1. GET DATA
        distance_map = frame.depth_data       # The 3D distances in millimeters
        ir_image = frame.amplitude_data       # The 2D Black and White picture

        # Convert the B&W picture so we can draw the green crosshair on it
        amp_8bit = cv2.normalize(ir_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        display_img = cv2.cvtColor(amp_8bit, cv2.COLOR_GRAY2BGR)

        # 2. FIND THE DEAD CENTER OF THE FRAME
        # Get the height (h) and width (w) of the sensor resolution
        h, w = distance_map.shape
        center_y = int(h / 2)
        center_x = int(w / 2)

        # 3. CALCULATE THE AVERAGE CENTER DISTANCE
        # Grab a tiny 5x5 pixel box right in the center of the screen
        center_box = distance_map[center_y-2:center_y+3, center_x-2:center_x+3]
        
        # Filter out any hardware glitches (0s) before doing the math
        valid_pixels = center_box[center_box > 0]
        
        if len(valid_pixels) > 0:
            center_distance = int(np.mean(valid_pixels))
        else:
            center_distance = 0 # Out of range or sensor error

        # 4. DRAW THE TARGET UI
        # Draw a crosshair
        cv2.line(display_img, (center_x - 15, center_y), (center_x + 15, center_y), (0, 255, 0), 2)
        cv2.line(display_img, (center_x, center_y - 15), (center_x, center_y + 15), (0, 255, 0), 2)
        
        # Draw a red dot directly in the center
        cv2.circle(display_img, (center_x, center_y), 3, (0, 0, 255), -1)

        # Print the live distance next to the crosshair
        text = f"{center_distance} mm"
        cv2.putText(display_img, text, (center_x + 20, center_y - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # 5. SHOW THE WINDOW
        cv2.imshow("ToF Center Trigger Sensor", display_img)
        
        cam.releaseFrame(frame)
            
        if cv2.waitKey(1) == 27: 
            break

    # --- GRACEFUL SHUTDOWN ---
    print("\nShutting down camera...")
    try:
        cam.stop()
    except Exception:
        pass
    try:
        cam.close()
    except Exception:
        pass
    cv2.destroyAllWindows()
    print("Safely exited.")

if __name__ == "__main__":
    main()