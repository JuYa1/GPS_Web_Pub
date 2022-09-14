import sys
import io
import rospy
from sensor_msgs.msg import NavSatFix
import rosbag
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine

class MyApp(QWidget):
   def __init__(self):
       super().__init__()
       self.setWindowTitle('Folium in PyQt')
       self.gps_data = [[0.0, 0.0]]

       layout = QVBoxLayout()
       self.setLayout(layout)

       # read_topic = 'sensor_msgs/NavSatFix'
       # test_bagfile = '/home/soju/snslab/gps_dcu2.bag'
       # self.bag_file = rosbag.Bag(test_bagfile)
       # for topic,msg,t in self.bag_file.read_messages(read_topic):

       rospy.init_node('gps_Su')
       gps = rospy.Subscriber('gps_data', NavSatFix, self.callback)

       coordinate = [35.9138, 128.8036]
       m = folium.Map(zoom_start=15,location=coordinate)

       data_gps = self.gps_data

       folium.Polygon(locations=data_gps, fill=True, tooltip='GPS').add_to(m)

       # save map data to data object
       data = io.BytesIO()
       m.save(data, close_file=False)

       webView = QWebEngineView()
       webView.setHtml(data.getvalue().decode())
       layout.addWidget(webView)

   def callback(self, msg):
       O_latitude = msg.latitude
       O_longitude = msg.longitude

       msg.latitude = int(str(O_latitude)[0:2]) + ((int(str(O_latitude)[2:4]) + O_latitude - int(O_latitude))/60)
       msg.longitude = int(str(O_longitude)[0:3]) + ((int(str(O_longitude)[3:5]) + O_longitude - int(O_longitude)) / 60)

       self.gps_data.append([msg.latitude, msg.longitude])
       print(self.gps_data)

       self.folium.Polygon(locations=self.gps_data, fill=True, tooltip='GPS').add_to(self.m)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   myApp = MyApp()
   myApp.show()
   sys.exit(app.exec_())
