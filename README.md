# 微博自动打印

## 功能：自动刷新指定用户的微博，当有新微博时通过打印机打印出来
## 实现方案：

总共分为两个定时逻辑
1. 定时刷新微博(crawl_dafa.py)
2. 定时检查打印(print_dafa.py)
刷新微博后存到mongodb中，供打印逻辑使用

## 相关文件介绍：
* 刷微博(blog_index.py)
    通过刷微博的H5页面的ajax接口(https://m.weibo.cn/api/container/getIndex)，得到json版的微博结构，详见附录
* 存储(result_saver.py)
    其实这里没有必要存储到数据库，可以每次和最开始的json做对比就可以了，但我这里还是用mongodb存起来了，因为我想留下所有的微博记录
* 还原(card_to_img.py)
    json版微博转换成图片，类似于截图，这里是先转成html，然后用[IMGKit](https://github.com/csquared/IMGKit)库转成图片，最后给打印机打印
* 打印(cups_printer.py)
    基于[cups](https://www.cups.org/)控制打印机，用到的命令就是 ` lpr -o media=Custom.WIDTHxLENGTHmm filename `
    我这里用的是一台热敏打印机，所以宽度是直接写死48mm的

## 使用方式：
参考 ` start.sh `

### 启动刷新微博：
``` python
python3 crawl_dafa.py 1307651590
```
指定刷新那个用户id的微博

### 启动定时检查打印：
``` python
python3 print_dafa.py 1307651590,6343201749
```
通过逗号隔开用户id


## 附录
* json版的微博
``` json
{
      "card_type": 9,
      "itemid": "1076031307651590_-_4136245053838604",
      "scheme": "https://m.weibo.cn/status/FfcTLg6AY?mblogid=FfcTLg6AY&luicode=10000011&lfid=1076031307651590&featurecode=20000320",
      "mblog": {
        "created_at": "08-02",
        "id": "4136245053838604",
        "mid": "4136245053838604",
        "idstr": "4136245053838604",
        "text": "今天早上五點 我做夢夢到笑醒 醒了還在笑 覺得沒有比這個更開心的起床方式了 我以後每天都要這樣起床 ​​​",
        "textLength": 94,
        "source": "iPhone 7 Plus",
        "favorited": false,
        "thumbnail_pic": "http://wx4.sinaimg.cn/thumbnail/4df12e06ly1fi56acrcpjj22lc1q8qv5.jpg",
        "bmiddle_pic": "http://wx4.sinaimg.cn/bmiddle/4df12e06ly1fi56acrcpjj22lc1q8qv5.jpg",
        "original_pic": "http://wx4.sinaimg.cn/large/4df12e06ly1fi56acrcpjj22lc1q8qv5.jpg",
        "is_vip_paid_status": false,
        "is_paid": false,
        "mblog_vip_type": 0,
        "user": {
          "id": 1307651590,
          "screen_name": "陳意涵",
          "profile_image_url": "https://tva1.sinaimg.cn/crop.0.0.180.180.180/4df12e06jw1e8qgp5bmzyj2050050aa8.jpg",
          "profile_url": "https://m.weibo.cn/u/1307651590?uid=1307651590&luicode=10000011&lfid=1076031307651590&featurecode=20000320",
          "statuses_count": 1645,
          "verified": true,
          "verified_type": 0,
          "verified_type_ext": 1,
          "verified_reason": "演员",
          "description": "每一件生活的小事　都有人分享的感覺還真是令人開心～ (工作請洽 1650777666@qq.com 林小姐)",
          "gender": "f",
          "mbtype": 12,
          "urank": 37,
          "mbrank": 6,
          "follow_me": false,
          "following": true,
          "followers_count": 18286243,
          "follow_count": 306,
          "cover_image_phone": "https://tva2.sinaimg.cn/crop.0.0.640.640.640/a1d3feabjw1ecasunmkncj20hs0hsq4j.jpg"
        },
        "picStatus": "0:1",
        "reposts_count": 1163,
        "comments_count": 2532,
        "attitudes_count": 94018,
        "isLongText": false,
        "liked": true,
        "visible": {
          "type": 0,
          "list_id": 0
        },
        "cardid": "star_419",
        "mblogtype": 0,
        "bid": "FfcTLg6AY",
        "pics": [
          {
            "pid": "4df12e06ly1fi56acrcpjj22lc1q8qv5",
            "url": "https://wx4.sinaimg.cn/orj360/4df12e06ly1fi56acrcpjj22lc1q8qv5.jpg",
            "size": "orj360",
            "geo": {
              "width": 405,
              "height": 270,
              "croped": false
            },
            "large": {
              "size": "large",
              "url": "https://wx4.sinaimg.cn/large/4df12e06ly1fi56acrcpjj22lc1q8qv5.jpg",
              "geo": {
                "width": 2048,
                "height": 1365,
                "croped": false
              }
            }
          }
        ]
      },
      "show_type": 0
    }
```
