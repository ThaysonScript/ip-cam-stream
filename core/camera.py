import os, cv2, urllib
import sys
from dotenv import load_dotenv
import requests
from intelbras_api.api import Api
from pyintelbras import IntelbrasAPI
from pyintelbras.helpers import parse_response


class Camera:
    def __init__(self):
        load_dotenv()

        self.camera_ip = os.getenv("CAMERA_IP")
        self.camera_user = os.getenv("CAMERA_USER")
        self.camera_password = os.getenv("CAMERA_PASSWORD")
        self.camera_password_formmat = urllib.parse.quote(os.getenv("CAMERA_PASSWORD"), safe='')

        self.intelbras = IntelbrasAPI(f"http://{self.camera_ip}")
        
        self.intelbras.login(f"{self.camera_user}", f"{self.camera_password_formmat}")
        
        self.api = Api()
        
    def __get_easy_url_request(self, method=None, action=None, **kwargs):
        """
        Constrói requisição com método e parâmetros flexíveis de forma facil
        """
        return getattr(self.intelbras, f'{method}')(action=action, **kwargs)
            
    
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
                
            

    def ptz_relative_movement(self, channel=1, rotate_base=0, rotate_lens=0, zoom=0):       
        response = self.__get_easy_url_request(
            method='ptz',
            action='moveRelatively',
            channel=channel,
            arg1=rotate_base,
            arg2=rotate_lens,
            arg3=zoom
        )
        print(self.api.get_with_digest(response.url, self.camera_user, self.camera_password))

                
                
obj = Camera()
# obj.rtp()
obj.ptz_relative_movement(zoom=-0.4)
# obj.get_snapshot()