from pyintelbras import IntelbrasAPI
from dotenv import load_dotenv
import os
import cv2
import urllib


class Camera:
    def __init__(self):
        load_dotenv()

        self.camera_ip = os.getenv("CAMERA_IP")
        self.camera_user = os.getenv("CAMERA_USER")
        self.camera_password = urllib.parse.quote(os.getenv("CAMERA_PASSWORD"), safe='')

        self.intelbras = IntelbrasAPI(f"http://{self.camera_ip}")
        
        self.intelbras.login(f"{self.camera_user}", f"{self.camera_password}")
        
    
    def rtp(self):       
        rtsp_url = self.intelbras.rtsp_url()
        
        cap = cv2.VideoCapture(rtsp_url)
        
        cv2.namedWindow("RTSP WINDOW", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("RTSP WINDOW", 800, 600)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("RTSP WINDOW", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
        
    def get_snapshot(self):
        response = self.intelbras.snapshot(channel=1, type=0)
        
        print(response.status_code)

        if response.status_code == 200:
            with open("img.jpeg", "wb") as bf:
                bf.write(response.content)
                
                
                
obj = Camera()
# obj.get_snapshot()
obj.rtp()