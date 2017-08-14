## url分析

**分类URL**
```
//分类页面
http://www.ireader.com/index.php?ca=booksort.index&pca=booksort.index&pid=92&cid=320&order=download&status=0&page=0

```
- pid频道 === 92 为出版图书 10 男频 68女频（其他数字都为出版）

- cid类型 === 小说 文学传记等（三位数字）

- status === 全部免费特价vip 0 1 2 3 4

-page === 分页页码


**详情URL**

```
http://www.ireader.com/index.php?ca=bookdetail.index&pca=booksort.index&bid=11251002

```
- bid === 书的id


## cookies分析

从浏览器中扒出来这三个
```
'Hm_lpvt_2583df02aa8541db9378beae2ed00ba0': '1502265076',
'Hm_lvt_2583df02aa8541db9378beae2ed00ba0': '1502263527',
'ZyId': 'ada56e4598ab89a9944f
```

## 爬取思路

掌阅书城页面结构
![image](http://note.youdao.com/yws/api/personal/file/F29F39B6FAB24494B2EF3A3CAFB13BAB?method=download&shareKey=8dc5e411c1529709998e35c2535b88bb)

关注三个点
1. 类型

    频道貌似只有三种，类型会随着频道的改变相应变化

2. 图书列表

    tab上的热门貌似只是改变排序，内容是一样的，获取每本书的detail地址，并根据此地址去解析详细内容

3. 分页

    只需要获取‘下一页’标签里的地址然后再次递归访问重复第二点方法


## 爬取内容

掌阅书城详情结构
![image](http://note.youdao.com/yws/api/personal/file/1315D363103449869FA1FC2CE6E7CEEE?method=download&shareKey=64366cf72abb979b162d3af18efac245)


```
{
    "_id" : "10107833",
    "author" : "周文根,徐之江",
    "img" : "http://book.img.ireader.com/group6/M00/17/13/CmQUN1X1A1CEOTvLAAAAAANWZNk701351932.jpg?v=PkHOJwXM",
    "title" : "市场营销与策划",
    "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=booksort.index&bid=10107833",
    "price" : "1.00元",
    "des" : "本书是市场营销专业的核心课程教材，以培训和训练学生的市场营销通用职业能力为宗旨，符合基于工作过程为导向的高职教育课程改革思路。\r\n本书注重实用性、应用性，帮助学生全面了解企业营销活动的基本内容，树立以顾客需求为导向的营销观念；能够完成相关的营销工作任务。",
    "num_rate" : "30",
    "rate" : "7.3",
    "tag" : "市场营销",
    "press" : "浙江大学出版社",
    "similar" : [
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10897498",
            "name" : "金融营销"
        },
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10863597",
            "name" : "商战(特劳特经典丛书)"
        },
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10885731",
            "name" : "保险销售人员超级口才训练：保险销售人员与客户的111次沟通实例 (莫萨营销沟系列 5)"
        },
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10878435",
            "name" : "项目计划、进度与控制（原书第5版）"
        },
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10907180",
            "name" : "案例：创业方法论（第16辑）"
        },
        {
            "url" : "http://www.ireader.com/index.php?ca=bookdetail.index&pca=bookdetail.index&bid=10956257",
            "name" : "零售心理战：要站在顾客的立场上思考"
        }
    ],
    "num_word" : "11.5万字"
}
```

爬取过程中发现对于有些字段要允许可以没有，因为页面上可能会没有相应字段




[leason|个人博客](http://www.leasonlove.cn/)