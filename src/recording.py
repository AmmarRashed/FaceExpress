import cv2

# Open the video file
video = cv2.VideoCapture('../InnerGenichiro.mkv')

# Set the starting frame number (e.g. 0 for the first frame)
frame_num = 0
video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

# Loop through the frames
while True:
    # Read the next frame
    ret, frame = video.read()

    # If the frame is not read correctly, break the loop
    if not ret:
        break

    # Do something with the frame (for example, display it)
    cv2.imshow('Frame', frame)
    cv2.waitKey(25)  # Change this value to adjust playback speed

    # Update the frame number
    frame_num += 1
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

# Release the video file and close the window
video.release()
cv2.destroyAllWindows()