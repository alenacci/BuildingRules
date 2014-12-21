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

xdotool key ctrl+shift+t
xdotool key Return
xdotool type "cd $cwd/simulator"
xdotool key Return
xdotool type "python run.py"
xdotool key Return

#copy the command
echo "wait time:5; trigger name:fire room_id:1; wait time:3; trigger name:fire room_id:2" | tr -d '\n' | xclip -selection clipboard
