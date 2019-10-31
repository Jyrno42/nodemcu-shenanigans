INTERFACE='wlx90f652065226'

ping -c4 192.168.0.1 > /dev/null

if [ $? != 0 ] 
then
  echo "No network connection, restarting $INTERFACE"
  /sbin/ifdown $INTERFACE
  sleep 5
  /sbin/ifup --force $INTERFACE
fi
