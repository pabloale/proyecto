#!/usr/bin/python

print("HOLIS A TODOS")

print("Acabe de saludar")


#sudo nano /etc/rc.local

#(sleep 10; bash -c 'python3 -u /home/pi/Desktop/helloworld.py 2>&1 | sudo tee -a /home/pi/Desktop/hello.out') &
#(sleep 10; bash -c 'python3 -u /home/pi/Desktop/MainThread.py 2>&1 | sudo tee -a /home/pi/Desktop/LumbSeat.out') &

#cat LumbSeat.out

#sudo ps -ax | grep MainThread

#sudo kill <pid>

#tail -f Desktop/LumbSeat.out

##========================================

#cd /home/pi
#cd .config
#mkdir autostart
#cd autostart
##/home/pi/.local/share/applications/realvnc-vncserverui-user.desktop
##Exec=vncserver-x11 -showstatus

#nano tightvnc.desktop 
##[Desktop Entry]
##Type=Application
##Name=TightVNC
##Exec=vncserver :1
##StartupNotify=false

##nano vncviewer.desktop
##[Desktop Entry]
##Name=VNC Viewer
##Type=Application
##Exec=xtightvncviewer 192.168.0.1 -p /home/pi/.vnc/passwd -fullscreen