cwd=$(pwd)

xdotool type "cd DangerCore"
xdotool key Return
xdotool key Return
xdotool type "python run.py"
xdotool key Return

xdotool key ctrl+shift+t
xdotool key Return
xdotool type "cd $cwd/VirtualSensor"
xdotool key Return
xdotool type "python run.py"
xdotool key Return

xdotool key ctrl+shift+t
xdotool key Return
xdotool type "cd $cwd/../../backend"
xdotool key Return
xdotool type "python run.py"
xdotool key Return


