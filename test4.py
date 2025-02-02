import json
import yt_dlp

# Load cookies from the JSON file
# with open('./temp/cookies.json', 'r') as file:
#     cookies = json.load(file)

# # Save cookies in a .txt format that yt-dlp can use
# cookie_file = 'cookies.txt'
# with open(cookie_file, 'w') as f:
#     for cookie in cookies:
#         # Construct the cookie string based on the JSON format
#         cookie_str = f"{cookie['domain']}\tTRUE\t{cookie['path']}\t{cookie['secure']}\t{cookie['expiration']}\t{cookie['name']}\t{cookie['value']}\n"
#         f.write(cookie_str)
cookie_file="VISITOR_PRIVACY_METADATA=CgJJThIEGgAgKA%3D%3D;__Secure-3PSID=g.a000swiR5KuxNSkyVx9FdWfA5agKyvy2ORSVGgbFifquw6Y2rRbSaIQ9g_zGK8y-CK1jMOPtdgACgYKAcQSARcSFQHGX2MiutjZBuAs_7XDdFRoc4_UGxoVAUF8yKrw_zx__yBEe9RaKlkig4XD0076;GPS=1;YSC=Yb6Pm--PL-o;__Secure-1PSIDTS=sidts-CjEBmiPuTbaBhQ-3cHLfwbi7p1hmtXf25AkdoSVhYxDplqt9NGROkI5ru383gkifOql6EAA;__Secure-3PAPISID=hqmJlVAnrt5AeXpz/AjKVG7AwaeYF66xbr;__Secure-3PSIDCC=AKEyXzXmRVLoRg-cezA374yZfBFjkrootiDjK4IOvd3Cgo6w5RhLpY59onCkboI9qQlx3LSB;__Secure-3PSIDTS=sidts-CjEBmiPuTbaBhQ-3cHLfwbi7p1hmtXf25AkdoSVhYxDplqt9NGROkI5ru383gkifOql6EAA;LOGIN_INFO=AFmmF2swRQIgDg2jNnJ_Yq_Sa1GejaLUwgNTQi8-fl5SexSY_SQjaikCIQC7Zf_ps7xjp2EywZqCQF_qwsoEY5996FibFBnby-JjPg:QUQ3MjNmeFREZ1N4NmVlX3RnWDlENEFXdFVnRkd3Ny1EcDdRTUR2cDFlbDNIVjFNT1hQQUw1YndROV9TRjY5TzFqQW00Y1psT0hUbU1qNDE2NFVidmU3NFFhMC1SbkVSd0xVVmZZSDlWNHZaU3lrV0s2dk5YNzNvSlR4RGtCb200TE1vQXJEaTBsbnBUTktwaEYyc2VzT2lCR2VvcUZjUzl3;PREF=tz=UTC&f4=4000000;VISITOR_INFO1_LIVE=UbgArobEyRw"

# Set up yt-dlp options with the cookies file
video_url = 'https://www.youtube.com/watch?v=fyR9FZMN5C8'
ydl_opts = {
    'format': 'best',  # Download the best quality available
    'outtmpl': 'downloaded_video.mp4',  # Output filename
    'cookies': cookie_file,  # Pass cookies to yt-dlp
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("Download complete!")
