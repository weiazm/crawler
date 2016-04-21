echo "---------------- starting "$1" crawler------------------- "
xfce4-terminal  --title $1  -x bash -c "python /home/why/PycharmProjects/crawler/src/multicrawler/"$1"RunnableGetContent.py ; exec bash" --window
echo "Done!"