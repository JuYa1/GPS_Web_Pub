import sys
import io
import rospy
import time
from sensor_msgs.msg import NavSatFix
import rosbag
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer
from threading import Thread
from folium import plugins

class MyApp(QWidget):
   def __init__(self):
       super().__init__()
       self.setWindowTitle('Folium in PyQt')
       self.gps_data = [[35.91381, 128.80361]]

       self.layout = QVBoxLayout()
       self.setLayout(self.layout)

       test_bagfile = '/home/soju/snslab/gps_data.bag'
       self.bag_file = rosbag.Bag(test_bagfile)

       # ros thread
       self.bagthreadFlag = True
       self.bagthread = Thread(target=self.getbagfile)
       self.bagthread.start()

       self.mytimer = QTimer()
       self.mytimer.start(1000)  # 1초마다 차트 갱신 위함...
       self.mytimer.timeout.connect(self.get_data)


       self.coordinate = [35.9138, 128.8036]
       m = folium.Map(zoom_start=15,location=self.coordinate)
       print(self.gps_data)

       folium.Polygon(locations=self.gps_data, fill=True, tooltip='GPS').add_to(m)
       # self.folium.Polygon(locations=self.gps_data, fill=True, tooltip='GPS').add_to(m)

       # save map data to data object
       data = io.BytesIO()
       m.save(data, close_file=False)

       self.webView = QWebEngineView()
       self.webView.setHtml(data.getvalue().decode())
       self.layout.addWidget(self.webView)

   @pyqtSlot()
   def get_data(self):
       print("get data")
       self.layout.removeWidget(self.webView)

       map = folium.Map(zoom_start=15, location=self.coordinate)
       # print(self.m)
       #folium.Polygon(locations=self.gps_data, fill=True, tooltip='GPS').add_to(map)
       folium.PolyLine(locations=self.gps_data, fill=False, tooltip='GPS').add_to(map)

       data = io.BytesIO()
       map.save(data, close_file=False)
       self.webView = QWebEngineView()
       self.webView.setHtml(data.getvalue().decode())
       self.layout.addWidget(self.webView)
       time.sleep(0.01)

       # print(self.gps_data)
       # time.sleep(1)

   def getbagfile(self):
       print("getbagfile init")

       read_topic = '/gps_data'  # 메시지 타입
       for topic, msg, t in self.bag_file.read_messages(read_topic, start_time=rospy.Time()):
           O_latitude = msg.latitude
           O_longitude = msg.longitude

           msg.latitude = int(str(O_latitude)[0:2]) + ((int(str(O_latitude)[2:4]) + O_latitude - int(O_latitude)) / 60)
           msg.longitude = int(str(O_longitude)[0:3]) + ((int(str(O_longitude)[3:5]) + O_longitude - int(O_longitude)) / 60)

           self.gps_data.append([msg.latitude, msg.longitude])

           # self.folium.Polygon(locations=self.gps_data, fill=True, tooltip='GPS').add_to(self.m)

           # time.sleep(0.1)  # 빨리 볼라면 주석처리 하면됨

if __name__ == '__main__':
   app = QApplication(sys.argv)
   myApp = MyApp()
   myApp.show()
   sys.exit(app.exec_())
