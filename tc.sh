#!/bin/bash
#
#  tc uses the following units when passed as a parameter.
#  kbps: Kilobytes per second 
#  mbps: Megabytes per second
#  kbit: Kilobits per second
#  mbit: Megabits per second
#  bps: Bytes per second 
#       Amounts of data can be specified in:
#       kb or k: Kilobytes
#       mb or m: Megabytes
#       mbit: Megabits
#       kbit: Kilobits
#  To get the byte figure from bits, divide the number by 8 bit
#
TC=/usr/sbin/tc
IF=wlp2s0		    # Interface 
DNLD=1mbps          # DOWNLOAD Limit
#UPLD=0.5mbps          # UPLOAD Limit 
IP=10.190.88.29     # Host IP
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"
 
start() {

#    $TC qdisc add dev $IF root handle 1: htb default 30
#    $TC class add dev $IF parent 1: classid 1:1 htb rate $DNLD
#    $TC class add dev $IF parent 1: classid 1:2 htb rate $UPLD
#    $U32 match ip dst $IP/32 flowid 1:1
#    $U32 match ip src $IP/32 flowid 1:2
    $TC qdisc add dev $IF handle ffff: ingress
    $TC filter add dev $IF parent ffff: protocol ip prio 50 u32 match ip dst \
         0.0.0.0/0 police rate ${DNLD} burst 10k drop flowid :1
#    $TC filter add dev $IF parent 1: protocol ip prio 50 u32 match ip src $IP/32 police rate $DNLD burst 10k drop flowid :1

}

stop() {

    #$TC qdisc del dev $IF root
    $TC qdisc del dev $IF ingress

}

restart() {

    stop
    sleep 1
    start

}

show() {

    $TC -s qdisc ls dev $IF

}

case "$1" in

  start)

    echo -n "Starting bandwidth shaping: "
    start
    echo "done"
    ;;

  stop)

    echo -n "Stopping bandwidth shaping: "
    stop
    echo "done"
    ;;

  restart)

    echo -n "Restarting bandwidth shaping: "
    restart
    echo "done"
    ;;

  show)
    	    	    
    echo "Bandwidth shaping status for $IF:\n"
    show
    echo ""
    ;;

  *)

    pwd=$(pwd)
    echo "Usage: $(/usr/bin/dirname $pwd)/tc.bash {start|stop|restart|show}"
    ;;

esac

exit 0

