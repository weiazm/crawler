echo "-------------------------------------------------------------------"
echo "-------- starting all crawlers from 1 to 18 ---------- "
i=1
while(($i<19))
do
bash restart.sh $i
i=$(($i+1))
done
echo "start all crawler done!"
xfce4-terminal  --title monitor  -x bash -c "python monitor.py  ; exec bash" --window
echo "start monitor done!"