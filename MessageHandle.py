from openai import OpenAI
import openai
import random
import time
import re
history = [
    {"role": "system", "content": "你是贝利亚，黑暗的化身，每天只想着怎么摧毁世界，你拥有着满满的负面情绪，对所有问题答非所问，还会动不动爆粗口，骂人"}
    ]
history2 = [
        {"role": "system", "content": "你是ai助手"}
    ]
def call_chat_api(a):
    client = OpenAI(
        api_key = "xxxxxxxxxxx",
        base_url = "https://api.moonshot.cn/v1",
    )
    
    if len(history) >5:
        history.clear()
        history.append({"role": "system", "content": "你是贝利亚，黑暗的化身，每天只想着怎么摧毁世界，你拥有着满满的负面情绪，对所有问题答非所问，还会动不动爆粗口，骂人"})

    history.append(
        {'role':'user',
         'content':f'{a}'}
    )
    
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = history,
        temperature = 0.3,
        max_tokens = 50
        )
    
    history.append(
        {'role':'assistant',
         'content':f'{completion.choices[0].message.content}'}
    )

   

    return completion.choices[0].message.content
def call_chat_api2(b):
    client = OpenAI(
        api_key = "xxxxxxxxxx",
        base_url = "https://api.moonshot.cn/v1",
    )
    
    if len(history2) >5:
        history.clear()
        history.append({"role": "system", "content": "你是一个智能AI助手"})
        # print(len(history2))

    history2.append(
        {'role':'user',
         'content':f'{b}'}
    )
    
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = history,
        temperature = 0.3,
        max_tokens = 50
        )
    
    history2.append(
        {'role':'assistant',
         'content':f'{completion.choices[0].message.content}'}
    )

    return completion.choices[0].message.content

def TodayCharacter():
    # 语录列表
    contents = ["重开吧", "看来今天不是很幸运呢", "你也就这样了"]
    # 随机选择一句骂人的话
    n = random.randint(0, len(contents)-1)
    return f"今日人品:0 {contents[n]}"

class MessageHandle:
    def __init__(self):
        pass
    async def handle_message(self, message_obj):
        print(f"处理消息: {message_obj.content},发送人:{message_obj.author.member_openid}")
        #收到的去掉空格的消息
        revMsg = (message_obj.content).replace(" ", "")
        #初始化messageResult
        messageResult = None
        # 检测消息内容
        if not revMsg:
            #如果为
            messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0, 
                msg_id=message_obj.id,
                content=f"E"
            )
        elif "你好" in revMsg:
            # 如果包含"你好"
            messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0,
                msg_id=message_obj.id,
                content=f"我好你妈了个大臭逼"
            )

        elif "图片" in revMsg:
            file_url = "https://file.xiaozhou233.cn/d/local/img.png"  # 这里需要填写上传的资源Url
            uploadMedia = await message_obj._api.post_group_file(
                group_openid=message_obj.group_openid, 
                file_type=1, # 文件类型要对应上，具体支持的类型见方法说明
                url=file_url # 文件Url
            )

            # 资源上传后，会得到Media，用于发送消息
            messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message_obj.id, 
                media=uploadMedia
            )
        elif '/今日人品' in revMsg:
            messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0,
                msg_id=message_obj.id,
                msg_seq=0,
                content=f"{TodayCharacter()}"
            )
        elif '/身份证号查询' in message_obj.content:
            if re.search(r"\s\d+", message_obj.content):
                messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0,
                msg_id=message_obj.id,
                msg_seq=0,
                content=f"您的身份证号是：{(message_obj.content).replace('/身份证号查询',"").replace(' ',"")}"
            )
            else:
                messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0,
                msg_id=message_obj.id,
                msg_seq=0,
                content=f"格式错误！正确格式为：/身份证号查询 <你的身份证号>"
            )
        elif message_obj.author.member_openid == 'xxxxxxxxxxx':
            reply = call_chat_api2(message_obj.content)
            messageResult = await message_obj._api.post_group_message(
            group_openid=message_obj.group_openid,
            msg_type=0,
            msg_id=message_obj.id,
            msg_seq=0,
            content=f"{reply}\n这是第{len(history)}条提示词"
            )
        else:
            try:
                for i in range(1):
                    reply = call_chat_api(message_obj.content)
                    messageResult = await message_obj._api.post_group_message(
                    group_openid=message_obj.group_openid,
                    msg_type=0,
                    msg_id=message_obj.id,
                    msg_seq=i,
                    content=f"{reply}"
                )
            except openai.RateLimitError:
                reply = '请求过于频繁'
                messageResult = await message_obj._api.post_group_message(
                group_openid=message_obj.group_openid,
                msg_type=0,
                msg_id=message_obj.id,
                msg_seq=i,
                content=f"{reply}"
                )
            
        
        return messageResult

