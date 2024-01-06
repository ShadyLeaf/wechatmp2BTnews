import json
import os
import re
import shutil
import subprocess
from io import BufferedReader, BytesIO
from time import sleep

import requests


def upload_image(image_path, image_upload_url, access_token, use_proxy=True):
    with open(image_path, "rb") as f:
        file_in_memory_bytes = BytesIO(f.read())
    file_in_memory_bytes.name = os.path.basename(image_path)
    file_in_memory = BufferedReader(file_in_memory_bytes)
    if use_proxy:
        proxies = {
            "http": "http://localhost:7890",
            "https": "http://localhost:7890",
        }
    else:
        proxies = None
    result = requests.post(
        url=image_upload_url,
        headers={
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
        },
        files={"file": file_in_memory},
        proxies=proxies,
    )
    resultjson = result.json()
    return resultjson["data"]["links"]["url"]


## Settings
with open("./config.json", "r") as f:
    data = json.load(f)

news_mp_url = data["news_mp_url"]
article_type = data["article_type"]
episode = data["episode"]

use_proxy = data["use_proxy"]
image_upload_url = data["image_upload_url"]
token = data["token"]

## prepare environment
print("Preparing......")
tool_folder_path = "./tool"
if not os.path.exists(tool_folder_path):
    os.makedirs(tool_folder_path)
data_folder_path = "./data"
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)
temp_folder_path = "./temp"
if not os.path.exists(temp_folder_path):
    os.makedirs(temp_folder_path)

proxies = {
    "http": "http://localhost:7890",
    "https": "http://localhost:7890",
}
file_path = "./tool/wechatmp2markdown-v1.1.5_win64.exe"
if not os.path.exists(file_path):
    wechatmp2md_url = "https://github.com/fengxxc/wechatmp2markdown/releases/download/v1.1.5/wechatmp2markdown-v1.1.5_win64.exe"
    if use_proxy:
        response = requests.get(wechatmp2md_url, proxies=proxies)
    else:
        response = requests.get(wechatmp2md_url)
    with open(file_path, "wb") as f:
        f.write(response.content)
        f.close()

# download article to ./temp as markdown
print("Downloading article from", news_mp_url)
subprocess.run(file_path + " " + news_mp_url + " " + temp_folder_path + " --image=save")
print("Article Downloaded.")
news_name = os.listdir(temp_folder_path)[0]
news_path = temp_folder_path + "/" + news_name
md_path = news_path + "/" + news_name + ".md"

# upload image to image host
print("Uploading image via", image_upload_url)
with open(md_path, "r", encoding="UTF-8") as f:
    text = f.read()
image_regex = r"!\[(.*?)\]\((.*?)\)"
images = re.findall(image_regex, text)
count = 0
for _, url in images:
    count += 1
    print("uploading:", url, end="    ")
    image_host_url = upload_image(
        image_path=news_path + "/" + url,
        image_upload_url=image_upload_url,
        access_token=token,
    )
    print("image host url:", image_host_url)
    image_regex_url = r"!\[.*?\]\(" + url + r"\)"
    replace = (
        "![" + article_type + episode + "-" + str(count) + "](" + image_host_url + ")"
    )
    text = re.sub(image_regex_url, replace, text)
    sleep(1)
print("Uploading complete")

# save result markedown file
with open(
    data_folder_path + "/" + article_type + episode + ".md", "w", encoding="UTF-8"
) as f:
    f.write(text)
print("Article saved to", data_folder_path + "/" + article_type + episode + ".md")

# clear temp files
shutil.rmtree(news_path)
print("temp file removed. All done.")
