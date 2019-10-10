#Importing libraries and packages
import face_recognition
import cv2
import numpy as np
from PIL import Image
import os
import re
import click
import pandas as pd

def Detect():
	#Access primary camera
	video_capture = cv2.VideoCapture(0)

	#Making lists of the known persons
	known_face_names = []
	known_face_encodings = []

	#Extract images from the folder in which this program is saved
	def image_files_in_folder(folder):
	    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

	#Train the images by there names and append in lists
	for file in image_files_in_folder("Images"):
	    basename = os.path.splitext(os.path.basename(file))[0]
	    img = face_recognition.load_image_file(file)
	    encodings = face_recognition.face_encodings(img)

	    if len(encodings) > 1:
	        click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

	    if len(encodings) == 0:
	        click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
	    else:
	        known_face_names.append(basename)
	        known_face_encodings.append(encodings[0])

	#Initialize lists for storing recorded data
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	#Making dictionary of persons to check weather they present or not
	d = {}
	for person in known_face_names:
		d[person] = 0

	#Starting the camera
	while True:
	    ret, frame = video_capture.read()

	    #Small the frame for better results
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #0.25

	    rgb_small_frame = small_frame[:, :, ::-1]

	    #Here detects the face and recognize it
	    if process_this_frame:
	        face_locations = face_recognition.face_locations(rgb_small_frame)
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	        face_names = []
	        for face_encoding in face_encodings:
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	          	#If not match the Unknown
	            name = "Unknown"
	            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
	            best_match_index = np.argmin(face_distances)
	            if matches[best_match_index]:
	                name = known_face_names[best_match_index]

	            #If name matches appens in list for showing in camera the name
	            #and make it present in the diction by increment the value of that name
	            face_names.append(name)
	            if name != "Unknown":
	            	d[name] += 1

	    #For making it loop
	    process_this_frame = not process_this_frame

	    #Making rectangle and print the name
	    for (top, right, bottom, left), name in zip(face_locations, face_names):

	    	#Making the photo 1/4th
	        top *= 4
	        right *= 4
	        bottom *= 4
	        left *= 4

	        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
	        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	        font = cv2.FONT_HERSHEY_DUPLEX
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	        #When the person is confirmed present then red color turns into green
	        if name == "Unknown":
	        	continue
	        elif d[name] >= 10:
	        	cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
	        	cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
	        	font = cv2.FONT_HERSHEY_DUPLEX
	        	cv2.putText(frame, "Present", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1) #name
	    cv2.imshow('Video', frame)

	    #For stop the camera press q
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	#This is for save the data in excel sheet
	ls_names = []
	ls_status = []
	for i,j in sorted(d.items()):
		ls_names.append(i)
		if j > 10:
			ls_status.append("Present")
		else:
			ls_status.append("Absent")
	data = {"Name":ls_names,
			"Status":ls_status}
	df = pd.DataFrame.from_dict(data)
	# print(df.head())
	df.to_excel("Attendence.xlsx")

	video_capture.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	Detect()