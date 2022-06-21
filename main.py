import os
import sys
from os import system
import threading
import random
import time
import requests
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


os.system('cls')
os.system(f"title Tikload ^| HengSok ^| Status: Running")
print(f"""
                    {Fore.CYAN}▀█▀ █ █▄▀ ▀█▀ █▀█ █▄▀   █▀▄ █▀█ █░█░█ █▄░█ █░░ █▀█ ▄▀█ █▀▄ █▀▀ █▀█
                    {Fore.CYAN}░█░ █ █░█ ░█░ █▄█ █░█   █▄▀ █▄█ ▀▄▀▄▀ █░▀█ █▄▄ █▄█ █▀█ █▄▀ ██▄ █▀▄
                                        {Fore.RED}https://github.com/SokunHeng""")

while True:
    def getVideoData(video_id):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        }

        request_data = requests.get(
            f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{video_id}%5D", headers=headers).json()

        return request_data


    def downloadSingleVideo():
        with_watermark = None
        print(f"""
{Fore.YELLOW}Select An Option To Download the video :
    [{Fore.BLUE}1{Fore.YELLOW}] With Watermark
    [{Fore.BLUE}2{Fore.YELLOW}] Without Watermark\n""")
        while with_watermark != 1 and with_watermark != 2:
            with_watermark = int(input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}]{Fore.RED} "))

        print()
        video_url = input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}] Video URL :{Fore.WHITE} ")

        video_id = video_url.split("/")[5]
        if "?" in video_url:
            video_id = video_id[:video_id.find('?')]

        if os.path.exists(f"./downloads/videos/{video_id}-wm.mp4") and with_watermark == 1:
            print(f"\n{Fore.YELLOW}===================================================================================")
            print(f"{Fore.YELLOW}[{Fore.RED}x{Fore.YELLOW}] Video Already Downloaded!")
            print(f"{Fore.YELLOW}===================================================================================")
            return
        if os.path.exists(f"./downloads/videos/{video_id}-no-wm.mp4") and with_watermark == 2:
            print(f"\n{Fore.YELLOW}===================================================================================")
            print(f"{Fore.YELLOW}[{Fore.RED}x{Fore.YELLOW}] Video Already Downloaded!")
            print(f"{Fore.YELLOW}===================================================================================")
            return

        data = getVideoData(video_id)

        if with_watermark == 1:
            download_url = data["aweme_details"][0]["video"]["download_addr"]["url_list"][0]
        else:
            download_url = data["aweme_details"][0]["video"]["play_addr"]["url_list"][0]

        with open(f'./downloads/videos/{video_id}-{"wm" if with_watermark == 1 else "no-wm"}.mp4', 'wb') as out_file:
            video_bytes = requests.get(download_url, stream=True)
            out_file.write(video_bytes.content)

        print(f"\n{Fore.YELLOW}===================================================================================")
        print(f"""{Fore.YELLOW}[{Fore.BLUE}✓{Fore.YELLOW}] Video Downloaded Successfully!""")
        print(f"{Fore.YELLOW}===================================================================================")


    def downloadVideoThumbnail():
        video_url = input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}] Video URL :{Fore.WHITE} ")

        video_id = video_url.split("/")[5]
        if "?" in video_url:
            video_id = video_id[:video_id.find('?')]

        if os.path.exists(f"./downloads/thumbnails/{video_id}-thumbnail.jpeg"):
            print(f"\n{Fore.YELLOW}===================================================================================")
            print(f"{Fore.YELLOW}[{Fore.RED}x{Fore.YELLOW}] Thumbnail Already Downloaded!")
            print(f"{Fore.YELLOW}===================================================================================")
            return

        data = getVideoData(video_id)

        download_url = data["aweme_details"][0]["video"]["origin_cover"]["url_list"][0]

        with open(f'./downloads/thumbnails/{video_id}-thumbnail.jpeg', 'wb') as out_file:
            image_bytes = requests.get(download_url)
            out_file.write(image_bytes.content)

        print(f"\n{Fore.YELLOW}===================================================================================")
        print(f"{Fore.YELLOW}[{Fore.BLUE}✓{Fore.YELLOW} Thumbnail Downloaded Successfully!")
        print(f"{Fore.YELLOW}===================================================================================")


    def downloadAllVidsFromUser():
        with_watermark = None
        print(f"""
{Fore.YELLOW}Select An Option To Download the video :
    [{Fore.BLUE}1{Fore.YELLOW}] With Watermark
    [{Fore.BLUE}2{Fore.YELLOW}] Without Watermark\n""")
        while with_watermark != 1 and with_watermark != 2:
            with_watermark = int(input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}]{Fore.RED} "))

        print()
        video_url = input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}] Insert One Video URL From the User :{Fore.WHITE} ")

        video_id = video_url.split("/")[5]
        if "?" in video_url:
            video_id = video_id[:video_id.find('?')]

        data = getVideoData(video_id)

        sec_uid = data["aweme_details"][0]["author"]["sec_uid"]

        request_url = f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/post/?sec_user_id={sec_uid}&count=33&device_id=9999999999999999999&max_cursor=0&aid=1180"
        request_headers = {
            "accept-encoding": "gzip",
            "user-agent": "com.ss.android.ugc.trill/240303 (Linux; U; Android 12; en_US; Pixel 6 Pro; Build/SP2A.220405.004;tt-ok/3.10.0.2)",
            "x-gorgon": "0"
        }
        request_data = requests.get(request_url, headers=request_headers).json()

        username = request_data["aweme_list"][0]["author"]["unique_id"]
        if not os.path.exists(f"./downloads/users/{username}"):
            os.makedirs(f"./downloads/users/{username}")
        if not os.path.exists(f"./downloads/users/{username}/wm"):
            os.makedirs(f"./downloads/users/{username}/wm")
        if not os.path.exists(f"./downloads/users/{username}/no-wm"):
            os.makedirs(f"./downloads/users/{username}/no-wm")

        videos = request_data["aweme_list"]

        print(f"""{Fore.RED}@{username} {Fore.YELLOW}Have {Fore.BLUE}{len(videos)} {Fore.YELLOW}Published Videos. Downloading them... Already Downloaded Videos Will Be Skipped.\n""")

        count = 0

        if with_watermark == 1:
            for video in videos:
                count += 1

                download_url = video["video"]["download_addr"]["url_list"][0]
                uri = video["video"]["download_addr"]["uri"]

                if os.path.exists(f"./downloads/users/{username}/wm/{uri}.mp4"):
                    print(
                        f"{Fore.YELLOW}[{Fore.RED}x{Fore.YELLOW}] Video Number {count} already Exists! Skipping It...")
                    continue

                with open(f'./downloads/users/{username}/wm/{uri}.mp4', 'wb') as out_file:
                    video_bytes = requests.get(download_url, stream=True)
                    out_file.write(video_bytes.content)
                    print(f"{Fore.YELLOW}[{Fore.BLUE}{count}{Fore.YELLOW}] Video Downloaded")
        else:
            for video in videos:
                count += 1

                download_url = video["video"]["play_addr"]["url_list"][0]
                uri = video["video"]["play_addr"]["uri"]

                if os.path.exists(f"./downloads/users/{username}/no-wm/{uri}.mp4"):
                    print(
                        f"{Fore.YELLOW}[{Fore.RED}x{Fore.YELLOW}] Video Number {count} already Exists! Skipping It...")
                    continue

                with open(f'./downloads/users/{username}/no-wm/{uri}.mp4', 'wb') as out_file:
                    video_bytes = requests.get(download_url, stream=True)
                    out_file.write(video_bytes.content)
                    print(f"{Fore.YELLOW}[{Fore.BLUE}{count}{Fore.YELLOW}] Video Downloaded")

        print()
        print(f"\n{Fore.YELLOW}===================================================================================")
        print(f"{Fore.YELLOW}[{Fore.BLUE}✓{Fore.YELLOW}] Successfully Updated/Downloaded  {Fore.BLUE}{count}  {Fore.YELLOW}Videos From {Fore.RED}@{username}")
        print(f"{Fore.YELLOW}===================================================================================")
        
    def downloadAudio():
        print(f"\n{Fore.YELLOW}Coming Soon!")
    def downloadUserProfilePicture():
        print(f"\n{Fore.YELLOW}Coming Soon!")

    if __name__ == "__main__":
        if not os.path.exists("./downloads"):
            os.makedirs("./downloads")
        if not os.path.exists("./downloads/videos"):
            os.makedirs("./downloads/videos")
        if not os.path.exists("./downloads/thumbnails"):
            os.makedirs("./downloads/thumbnails")

        print(f"""    
{Fore.YELLOW}Select An Option :
    [{Fore.BLUE}1{Fore.YELLOW}] Download Single Video
    [{Fore.BLUE}2{Fore.YELLOW}] Download Video Thumbnail
    [{Fore.BLUE}3{Fore.YELLOW}] Download All Videos From User
    [{Fore.BLUE}4{Fore.YELLOW}] Download Audio ({Fore.RED}Upcoming{Fore.YELLOW})
    [{Fore.BLUE}5{Fore.YELLOW}] Download User Profile Picture ({Fore.RED}Upcoming{Fore.YELLOW})
    [{Fore.BLUE}6{Fore.YELLOW}] Close the Script\n""")
        choice = None
        while choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5 and choice != 6:
            choice = int(input(f"{Fore.YELLOW}[{Fore.BLUE}=>{Fore.YELLOW}]{Fore.RED} "))

        if choice == 1:
            downloadSingleVideo()
        elif choice == 2:
            downloadVideoThumbnail()
        elif choice == 3:
            downloadAllVidsFromUser()
        elif choice == 4:
            downloadAudio()
        elif choice == 5:
            downloadUserProfilePicture()
        elif choice == 6:
            sys.exit()
        else:
            print("Invalid input, please try again!")
