# import yt_dlp
 
# # 输入要下载的YouTube视频地址
# url='https://www.youtube.com/watch?v=SAL-mNE10TA'
# ydl_opts={
#     'outtmpl': '指定的路径/123.mp4'
#     }
 
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# 	ydl.download([url])
 
# print("Video downloaded successfully!")


# # https://www.youtube.com/watch?v=SAL-mNE10TA


##https://developers.google.com/youtube/v3/docs?hl=zh-cn


import yt_dlp
import requests
import json
import os
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime

class yt_video:
    #配置参数
    def __init__(self,page,word,API_key):
        #关键词
        self.word = word
        # 请求地址
        self.url = 'https://youtube.googleapis.com/youtube/v3/search'
        #视频地址前缀
        self.video_url = 'https://www.youtube.com/watch?v='
        # 生成随机的用户代理
        ua = UserAgent()
        user_agent = ua.random
        # 请求头
        self.headers = {
            "Accept": "*/*",
            "User-Agent": user_agent
                }
        # 请求参数,其他参数看官网文档修改或增加即可
        self.params = {
            'part': 'snippet',
            'maxResults': '25',
            'q': self.word,
            'key': API_key,
            'order': 'date',
            "pageToken":'',
            'type':'video'
                }
        #存response_json的列表容器
        self.res_lst = []
        #页数
        self.page = int(page)
        #获取当前脚本所在的路径
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        #存字典的容器
        self.dict_lst = []
        # 获取当前时间
        # 格式化时间为'2024_01_02_03_04_05'形式,年_月_日_时_分_秒形式
        current_time = datetime.now()
        self.formatted_time = current_time.strftime('%Y_%m_%d_%H_%M_%S')  
        #创建存视频的文件夹路径
        self.folder_path = self.current_dir + '/' + self.formatted_time
        os.makedirs(self.folder_path, exist_ok=True)
        
    
    #启动请求函数
    def start_requests(self):
        
        for _ in range(self.page):  #取数据的页数，默认一页25条
            res = requests.get(url=self.url, headers=self.headers, params=self.params)
            response = json.loads(res.text)
            self.res_lst.extend(response['items'])
            
            if 'nextPageToken' in response:
                self.params['pageToken'] = response['nextPageToken']
            else:
                break
                   
        for video in self.res_lst:
            # 创建一个空字典
            author_dict = {} 
            author_dict['作者'] = video['snippet']['channelTitle']
            author_dict['标题'] = video['snippet']['title']
            author_dict['描述/类型'] = video['snippet']['description']
            author_dict['发布时间'] = video['snippet']['publishTime']
            author_dict['封面图片地址'] = video['snippet']['thumbnails']['high']['url']
            author_dict['视频id'] = video['id']['videoId']
            author_dict['视频地址'] = self.video_url + video['id']['videoId']
            self.dict_lst.append(author_dict)
        df = pd.DataFrame(self.dict_lst)

        # 要生成的文件名
        json_file_path = os.path.join(self.current_dir, 'result.json')
        csv_file_path = os.path.join(self.current_dir, self.formatted_time+self.word+'.csv')
        #把json存文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.res_lst, f, ensure_ascii=False, indent=4)
            
        #把df存csv文件
        df.to_csv(csv_file_path, encoding='utf-8-sig', index=False)
            
        print(df)
        
        #循环下载每一个视频
        for index, row in df.iterrows():
            try:
                self.download(row['视频地址'],row['标题'])
                print("##################################################################")
            except Exception as e:
                print(row['标题'])
                print("Video downloaded error!:---" + str(e))
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                
                
        return df
                

    def download(self,download_url,title):
        #保存路径,标题作为视频名字
        title = title.replace('/','|')
        ydl_opts={
            'outtmpl': self.folder_path + '/'+ title + '.mp4',
            'cookiefile': 'cookies.txt'
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_url])
        
        return "Video downloaded successfully!" 
        
    
if __name__ == '__main__':
    #页数
    page = '1'
    #关键词
    word = '小米su7'
    #你的apikey
    api_key = ''
    #按顺序传参:页数,关键词,你的apikey
    result = yt_video(page,word,api_key)
    
    a = result.start_requests()
    
    print(a['标题'])
    
