本代码是google开放api和yt_dlp库结合起来实现的，youtube视频自动化批量搬运

你需要去api官网自助申请好api key，带着你申请的apikey发送请求拿到每条视频的id，拼接成完整视频地址

再用完成视频地址使用yt_dlp库去下载到你指定的文件夹

https://console.cloud.google.com/apis/api/youtube.googleapis.com/metrics

![image](https://github.com/user-attachments/assets/84633642-fc90-4a45-8175-10ee2ae6e2ae)

api文档地址

https://developers.google.com/youtube/v3/docs/search/list?hl=zh-cn

你可以按照文档里提供的参数，自由定制要获取的视频类型

另外你需要用浏览器的get cookie插件把cookie粘贴到cookie.txt文件中

![image](https://github.com/user-attachments/assets/b330267c-d47d-4f5b-9455-733500fb60be)


![image](https://github.com/user-attachments/assets/9658be11-25ed-495b-b22f-a822fb8bcea1)



