"""
    将solr中数据迁移到另外一个solr中

    生成uuid：
    uuid.NAMESPACE_URL

    使用 pysolr 进行数据的导入
    pip install  pysolr

"""
import asyncio
import re
import uuid

import requests
import pysolr

# 上下文长度
CONTEXT_LENGTH = 15


async def get_solr_data(solr_client, start, rows):
    """
     获取solr中数据 ，返回 json 数组

     {
        "pubId":19900460405,
        "zhTitle":"一种大承载高刚度静压气体轴承",
        "cabstract":"气体流动过程中在节流面(F2)处发生第二次节流作用。",
    }
    :param start:
    :param rows:
    :return:
    """
    params = {
        "start": start,
        "rows": rows,
        "indent": "on",
        "wt": "json",
        "fl": "pubId, zhTitle, cabstract",
    }

    results = solr_client.search(q="type:2", **params)
    return results.docs


def handle_solr_data(docs):
    """
    {
        "id":"d9794be8-d927-461b-b28a-42d8bf16110a",
        "pubId":"100009606",
        "content":"研发项目可行性研究报告提纲 ",
        "segmentContext":"<em>研发项目可行性研究报告提纲 </em>\n \n \n \n \n \n项目名称：环保物联",
        "sysType":22,
        "title":"环保物联网排污权交易总量管理控制一体机",
    }
    :param docs:
    :return:
    """
    segment_list = []

    for doc in docs:
        c_abstract = doc["cabstract"]
        zh_title = doc["zhTitle"]
        pub_id = doc["pubId"]

        dict_list = get_segment_context(pub_id, zh_title, c_abstract)

        segment_list.extend(dict_list)

    return segment_list


async def update_to_solr(update_solr_client, dict_list):
    """
    :param update_solr_client:
    :param dict_list:
    :return:
    """
    r = update_solr_client.add(dict_list)
    return r


def get_segment_context(pub_id, zh_title, content):
    """

    :param pub_id:
    :param zh_title:
    :param content: 论文或者项目内容
    :return:  内容中[{句子，句子上下文}]
    """

    pattern = ".+?[\r\n；;!！？?。]"
    matcher = re.compile(pattern)

    content_length = len(content)
    dict_list = []
    pos = 0
    while True:
        match = matcher.match(content, pos=pos)
        if not match:
            break
        segment = match.group()

        # 开始结束
        start = match.start()
        # 纠正 初始化点
        if (start - CONTEXT_LENGTH) < 0:
            start = 0
        else:
            start = start - CONTEXT_LENGTH

        end = match.end()
        if (end + CONTEXT_LENGTH) > content_length:
            end = content_length
        else:
            end = end + CONTEXT_LENGTH

        segment_context = content[start:end]

        # 从 0 开始
        pos += len(segment)

        dict_list.append({
            "segmentContext": segment_context,
            "content": segment,
            "id": str(uuid.uuid1()),
            "sysType": 22,
            "pubId": pub_id,
            "title": zh_title
        })

    return dict_list


SOLR_SELECT_URL = "http://192.168.15.13:8091/solr/solr_cores_high_new_tech"
SOLR_UPDATE_URL = "http://192.168.15.13:8091/solr/collection1"


async def task(start, rows):
    # 获取solr中数据
    select_solr_client = pysolr.Solr(url=SOLR_SELECT_URL)

    json_docs = await  get_solr_data(select_solr_client, start, rows)

    # 处理solr中数据
    segment_list = handle_solr_data(json_docs)

    # 保存到 solr
    update_solr_client = pysolr.Solr(url=SOLR_UPDATE_URL)
    resp = await update_to_solr(update_solr_client, segment_list)

    print("start:%d , rows:%d , response:%s" % (start, rows, resp))


def main():
    # 分配 task
    select_solr_client = pysolr.Solr(url=SOLR_SELECT_URL)
    num_found = select_solr_client.search(q="type:2").hits

    rows = 10
    start = 0
    tasks = []
    while start < num_found:
        tasks.append(task(start, rows))
        start += rows

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
