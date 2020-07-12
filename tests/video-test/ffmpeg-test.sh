pipenv run python test_send.py | ffplay -f jpeg_pipe -fflags nobuffer -pixel_format yuv420p -vcodec mjpeg -video_size 640x480 -framerate 30 -i -
# ffmpeg -f rawvideo -pixel_format bgr24 -video_size 640x480 -framerate 30 -i - foo.avi
# pipenv run python test_send.py | ffmpeg -v verbose \
#               -f rawvideo \
#               -video_size 640x480 \
#               -pixel_format bgr24 \
#               -framerate 30 \
#               -i - \
#               foo.avi
            #   -f mpegts udp://kleiber.xyz:4200

# -vcodec h264 \
# This works
# ffmpeg -v verbose \
#               -f v4l2 \
#               -i /dev/video0 \
#               -r 30 -g 0 -vcodec h264 -acodec libmp3lame \
#               -tune zerolatency \
#               -preset ultrafast \
#               -f mpegts udp://kleiber.xyz:4200