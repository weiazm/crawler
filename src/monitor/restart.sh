echo "---------------- starting "$1" crawler------------------- "
gnome-terminal -x bash -c "python /home/why/PycharmProjects/crawler/src/multicrawler/"$1"RunnableGetContent.py" --window
echo "Done!"