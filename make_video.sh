#!/bin/bash

cat *.jpg | ffmpeg -f image2pipe -framerate 30 -vcodec mjpeg -i - -vcodec libx264 out.mp4
