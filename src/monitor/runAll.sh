echo "------------------------------------------------------"
echo "-------- starting all crawlers from 1 to 18 ---------- "
echo ""
i=1
while(($i<19))
do
gnome-terminal -x bash -c "python /home/why/PycharmProjects/crawler/src/multicrawler/"$i"RunnableGetContent.py" --window
i=$(($i+1))
done
echo "Done!"
