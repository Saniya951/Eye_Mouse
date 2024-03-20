import cv2
import mediapipe
import pyautogui

# variable to store face landmarks
face_mesh_landmarks = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()  # to get teh mouse screen position on screen
while True:
    _,image =cam.read()
    image = cv2.flip(image,1) #for verical flip it is 1 and for horizontal flip it is 0
    #flipping image bcz landmarks are showing on right eye we want it on left eye
    window_h,window_w,_= image.shape
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  
    processed_image = face_mesh_landmarks.process(rgb_image)

    all_face_landmark_points = processed_image.multi_face_landmarks #storing all the face LANDMARKS

    if all_face_landmark_points:
        one_face_landmark_points = all_face_landmark_points[0].landmark
        for id,landmark_point in enumerate(one_face_landmark_points[474:478]):  #[] no is specified to show only 5 points
            x = int(landmark_point.x * window_w ) #for displaying  value on screen
            y = int(landmark_point.y * window_h )  #for displaying y valu on screen
            #print(x,y)  #print x and y values of landmark points

            if id==1:
                mouse_x = int(screen_w / window_w *x)
                mouse_y = int(screen_h / window_h *y)
                pyautogui.moveTo(mouse_x, mouse_y)
            cv2.circle(image,(x,y),3,(0,0,255)) #display color on screen for landmark points

        left_eye = [one_face_landmark_points[145], one_face_landmark_points[159]]  #two points for left eye
        for landmark_point in left_eye: 
            x = int(landmark_point.x * window_w ) #for displaying  value on screen
            y = int(landmark_point.y * window_h )  #for displaying y valu on screen
            #print(x,y)  #print x and y values of landmark points
            cv2.circle(image,(x,y),3,(0,255,255)) #display color on screen for landmark points

        #now for moving nd clicking 
        #calculating vertical distance btw left eye to know when eye is blink
        if(left_eye[0].y - left_eye[1].y<0.01):
            pyautogui.click()
            pyautogui.sleep(2) #wait for 2 sec
            print('mouse clicked')
    cv2.imshow("Eye Controlled mouse", image)
    key = cv2.waitKey(100) # to display screen
    if key ==27:
        break         #if esc press then shut then display
cam.release()       #if esc press then shut then display
cv2.destroyAllWindows()   #if esc press then shut then display

