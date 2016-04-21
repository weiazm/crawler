echo "-------------------------------------------------------------------"
echo "-------- starting all crawlers from 1 to 18 ---------- "
i=1
while(($i<19))
do
bash restart.sh $i
i=$(($i+1))
done
echo "start all crawler done!"
python monitor.py
echo "start monitor done!"