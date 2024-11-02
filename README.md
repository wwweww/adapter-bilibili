![assets\adapter-bilibili.png](https://socialify.git.ci/wwweww/adapter-bilibili/image?description=1&descriptionEditable=%E9%80%82%E9%85%8D%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E7%9B%B4%E6%92%AD%E9%97%B4websocket%E5%8D%8F%E8%AE%AE%E7%9A%84nonebot2%E9%80%82%E9%85%8D%E5%99%A8&font=Inter&forks=1&issues=1&logo=https%3A%2F%2Fgithub.com%2Fwwweww%2Fadapter-bilibili%2Fblob%2Fmain%2Fassets%2Fa.png%3Fraw%3Dtrue&name=1&pattern=Charlie%20Brown&stargazers=1&theme=Light)
# 配置
```
DRIVER=~websockets                # 必须有的正向ws的Driver
rooms=[123, 123, 123]             # 直播间房间号 
manual_login=true                 # 是否需要手动登录 (登录以后才可以用send方法向直播间发送消息) 默认false(还没实现)
bili_cookie="buvid***"            # 登录用的cookies (登录以后才可以用send方法向直播间发送消息) 默认"",没有配置将使用二维码登录
```
# 已实现事件
<details>
  <summary>消息类</summary>

`Danmu_msg`弹幕<br>
`Super_chat_message`醒目留言
</details>

<details>
  <summary>通知类</summary>
`Combo_send`连击礼物<br>
`Send_gift`投喂礼物<br>
`Common_notice_danmaku`限时任务<br>
`Entry_effect`舰长进房<br>
`Interact_word`普通进房消息<br>
`Guard_buy`上舰<br>
`User_toast_msg`续费舰长<br>
`Notice_msg`在本房间续费了舰长<br>
`Like_info_v3_click`点赞<br>
`Like_info_v3_update`总点赞数<br>
`Online_rank_count`在线等级统计<br>
`Room_change`房间信息变动<br>
`Room_real_time_message_update`房间数据<br>
`Watched_change`直播间实时观看人数<br>
`Stop_live_room_list`实时下播列表<br>
`Room_real_time_message_update`房间数据<br>
`Anchor_lot_start`天选之人开始<br>
`Anchor_lot_award`天选之人结果<br>

</details>

# 已实现api
`send` 发送弹幕

# ~~Todo~~(大饼):

- 登录制作
- 代码重构

# 鸣谢

- [ieew](https://github.com/ieew)： 提供代码上的帮助
- [17TheWord](https://github.com/17TheWord)： 教我使用github
- [NoneBot2](https://github.com/nonebot/nonebot2)： 开源代码 让我拥有这次学习机会

# 顺便一提
初出茅庐, 有啥好的意见or代码有啥bug欢迎提交
