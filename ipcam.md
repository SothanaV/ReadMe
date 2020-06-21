# Record Video From IpCam By FFmpeg
    ffmpeg -rtsp_transport tcp -i rtsp://admin:888888@192.168.88.254:10554/tcp/av0_0 -flags +global_header -f segment -segment_time 60 -segment_format_options movflags=+faststart -reset_timestamps 1 -f segment -segment_time 10 -segment_format mp4 "out%03d.mp4"
#
# Vstar cam
## IpCam VstarCam 
    path : rtsp://admin:888888@192.168.88.254:10554/tcp/av0_0
    User : admin
    Password : 888888

