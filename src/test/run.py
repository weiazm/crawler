# coding=utf-8
import os

command = 'deepin-terminal  -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"&' \
          'gnome-terminal -x bash -c "python test.py;exec bash"'
'gnome-terminal -t "title-name" -x bash -c "sh ./run.sh;exec bash;"'
os.system(command)
