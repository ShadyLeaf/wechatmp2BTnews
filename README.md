# wechatmp2BTnews

从微信公众号获取睡前消息文章，并上传图片至[Lsky Pro](https://github.com/lsky-org/lsky-pro)图床

# 使用方法

## 运行环境
- Python3
- requests
## 配置config.json
```json
{
    "news_mp_url": "https://mp.weixin.qq.com/s/ruN55uyX03hQ0ttSTzkjHA",
    "article_type": "reference",
    "episode": "176",
    "use_proxy": true,
    "image_upload_url": "https://example.image.host/api/v1/upload",
    "token": "my image upload token"
}
```
- `news_mp_url`: 微信公众号文章链接，例: `https://mp.weixin.qq.com/s/ruN55uyX03hQ0ttSTzkjHA`
- `article_type`: 节目类型，与[bedtime.news](https://github.com/bedtimenews/bedtimenews-archive-contents)仓库目录对应，值包括`main`, `reference`, `daily`, `opinion`, `commercial`，用于给结果文件命名
- `episode`: 节目期数，用于给结果文件命名
- `use_proxy`: 上传和下载是否使用代理
- `image_upload_url`: 图床的上传API链接
- `token`: 图床认证token

## 运行

运行`main.py`即可

```shell
python main.py
```

结果保存在`./data/`目录下

# 感谢

公众号文章下载使用项目[wechatmp2markdown](https://github.com/fengxxc/wechatmp2markdown)