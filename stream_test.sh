#! /bin/bash

# streaming on Ubuntu via ffmpeg.
# see http://ubuntuguide.org/wiki/Screencasts for full documentation
# see http://www.thegameengine.org/miscellaneous/streaming-twitch-tv-ubuntu/
# for instructions on how to use this gist

if [ ! -f .stream_key ]; then
	echo "Error: Could not find file: ~/.twitch_key"
	echo "Please create this file and copy past your stream key into it. Open this script for more details."
   	 exit 1;
fi

# input resolution, currently fullscreen.
# you can set it manually in the format "WIDTHxHEIGHT" instead.
INRES=$(xwininfo -root | awk '/geometry/ {print $2}'i)

# output resolution.
# keep the aspect ratio the same or your stream will not fill the display.
OUTRES="640x360"

# input audio. You can use "/dev/dsp" for your primary audio input.
INAUD="pulse"

# target fps
FPS="30"

# video preset quality level.
# more FFMPEG presets avaiable in /usr/share/ffmpeg
# According to trac.ffmpeg.org/wiki/x264EncodingGuide the presets are ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
QUAL="fast"

# stream key. You can set this manually, or reference it from a hidden file like what is done here.
STREAM_KEY=$(cat .stream_key)

# stream url. Note the formats for twitch.tv and justin.tv
# twitch:"rtmp://live.twitch.tv/app/$STREAM_KEY"
STREAM_URL="rtmp://live.twitch.tv/app/$STREAM_KEY"

export DISPLAY=:0.0

raspivid \
	-t 0 \
	-w 960 -h 540 \
	-fps 30 -b 2000000 \
	-vf -o - | \
ffmpeg -i - -vcodec copy -an -f flv "$STREAM_URL"

#~/ffmpeg-bin/ffmpeg\
#    -debug \
#    -f video4linux2 -max_streams 100 -s 656x416 -r "$FPS" -i /dev/video0   \
#    -c:v libx264 -s "$OUTRES" -preset veryfast \
#    -threads 8 \
#    -f flv "$STREAM_URL"
