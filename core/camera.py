import cv2

from core.intelbras_api.api import Api
from pyintelbras.helpers import parse_response


class Camera:
    def __init__(self):      
        self.api = Api()
        
        
    def get_rtsp_stream(self):
        return self.api.intelbras.rtsp_url()
    
    
    def rtsp_viewer(self):        
        rtsp_url = self.api.intelbras.rtsp_url()
        
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
        intelbras_response_api = self.api.intelbras.snapshot(channel=1, type=0)

        if intelbras_response_api.status_code == 200:
            with open("img.jpeg", "wb") as bf:
                bf.write(intelbras_response_api.content)
           
           
    def ptz_get_capability_current_protocol(self, channel=1):
        '''
        method: GET
        
        request url: http://<server>/cgi-bin/ptz.cgi?action=getCurrentProtocolCaps
        
        request example: http://192.168.1.108/cgi-bin/ptz.cgi?action=getCurrentProtocolCaps&channel=1
        
        full doc example: docs/api/ptz/ptz_get_capability_current_protocol.md
        '''
        intelbras_response_api = self.api.get_easy_url_request(
            method='ptz',
            action='getCurrentProtocolCaps',
            channel=channel
        )

        intelbras_response_api = self.api.get_with_digest(intelbras_response_api.url, self.api.camera_user, self.api.camera_password)
    
        return {
            "status_code": intelbras_response_api.status_code,
            "url": intelbras_response_api.url,
            "text": parse_response(intelbras_response_api.text)
        }  
        
        
    def ptz_control_basic_movement(self, channel=1, code='Up', rotate_base=0, rotate_lens=0, zoom=0):
        '''
        method: GET
        
        request url: http://<server>/cgi-bin/ptz.cgi?action=start
        
        request example: http://192.168.1.108/cgi-bin/ptz.cgi?action=start&channel=1&code=Up&arg1=0&arg2=1&arg3=0
        
        response: OK
        
        full doc example: docs/api/ptz/control/ptz_control_basic_movement.md
        '''
        intelbras_response_api = self.api.get_easy_url_request(
            method='ptz',
            action='start',
            channel=channel,
            code=code,
            arg1=rotate_base,
            arg2=rotate_lens,
            arg3=zoom
        )

        intelbras_response_api = self.api.get_with_digest(intelbras_response_api.url, self.api.camera_user, self.api.camera_password)
    
        return {
            "status_code": intelbras_response_api.status_code,
            "url": intelbras_response_api.url,
            "text": parse_response(intelbras_response_api.text)
        }
    
    
    def ptz_control_stop_movement(self, code='Up', channel=1, rotate_base=0, rotate_lens=0, zoom=0):
        '''
        method: GET
        
        request url: http://<server>/cgi-bin/ptz.cgi?action=stop
        
        request example: http://192.168.1.108/cgi-bin/ptz.cgi?action=stop&code=Up&channel=1&arg1=0&arg2=0&arg3=0
        
        response: OK
        
        full doc example: docs/api/ptz/control/ptz_control_stop_movement.md
        '''
        intelbras_response_api = self.api.get_easy_url_request(
            method='ptz',
            action='stop',
            code=code,
            channel=channel,
            arg1=rotate_base,
            arg2=rotate_lens,
            arg3=zoom
        )

        intelbras_response_api = self.api.get_with_digest(intelbras_response_api.url, self.api.camera_user, self.api.camera_password)
    
        return {
            "status_code": intelbras_response_api.status_code,
            "url": intelbras_response_api.url,
            "text": parse_response(intelbras_response_api.text)
        }
    
    
    def ptz_control_continuosly_moving(self, code='Continuously', channel=1, rotate_base=0, rotate_lens=0, zoom=0, movement_time=3600):
        '''
        method: GET
        
        request url: http://<server>/cgi-bin/ptz.cgi?action=start&code=Continuously
        
        request example: http://192.168.1.108/cgi-bin/ptz.cgi?action=start&code=Continuously&channel=1&arg1=5&arg2=5&arg3=5&arg4=60
        
        response: OK
        
        full doc example: docs/api/ptz/control/ptz_control_continuosly_moving.md
        '''
        intelbras_response_api = self.api.get_easy_url_request(
            method='ptz',
            action='start',
            code=code,
            channel=channel,
            arg1=rotate_base,
            arg2=rotate_lens,
            arg3=zoom,
            arg4=movement_time
        )

        intelbras_response_api = self.api.get_with_digest(intelbras_response_api.url, self.api.camera_user, self.api.camera_password)
    
        return {
            "status_code": intelbras_response_api.status_code,
            "url": intelbras_response_api.url,
            "text": parse_response(intelbras_response_api.text)
        }
        
        
    def ptz_control_stop_continuosly_moving(self):
        pass
    
    
    def ptz_control_3d_positioning(self):
        pass
            

    def ptz_control_relative_movement(self, channel=1, rotate_base=0, rotate_lens=0, zoom=0):       
        '''
        method: GET
        
        request url: http://<server>/cgi-bin/ptz.cgi?action=moveRelatively
        
        request example: http://192.168.1.108/cgi-bin/ptz.cgi?action=moveRelatively&channel=1&arg1=0.1&arg2=0.1&arg3=0.5
        
        response: OK
        
        full doc example: docs/api/ptz/control/ptz_control_relative_movement.md
        '''
        intelbras_response_api = self.api.get_easy_url_request(
            method='ptz',
            action='moveRelatively',
            channel=channel,
            arg1=rotate_base,
            arg2=rotate_lens,
            arg3=zoom
        )

        intelbras_response_api = self.api.get_with_digest(intelbras_response_api.url, self.api.camera_user, self.api.camera_password)
    
        return {
            "status_code": intelbras_response_api.status_code,
            "url": intelbras_response_api.url,
            "text": parse_response(intelbras_response_api.text)
        }
        
        
    def ptz_control_accurate_positioning(self):
        pass