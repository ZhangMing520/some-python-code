"""
    将solr中数据迁移到另外一个solr中

    生成uuid：
    uuid.NAMESPACE_URL


    合并2个dict：
    merge_dict = dict(dict1,**dict2)
"""
import asyncio
import re
import uuid

import requests

# 上下文长度
CONTEXT_LENGTH = 15


def get_solr_data(solr_select_url, start, rows):
    """
     获取solr中数据 ，返回 json 数组

     {
        "pubId":19900460405,
        "zhTitle":"一种大承载高刚度静压气体轴承",
        "cabstract":"一种大承载高刚度静压气体轴承,由轴承体(1)、供气孔(2)、节流槽(3)和均压槽(4)组成,其特征在于：所述轴承体(1)表面设有扇形节流槽(3)和均压槽(4)。轴承工作时,轴承体(1)和止推板(6)之间形成气膜(5),供气孔(2)与节流槽(3)和均压槽(4)相连通,供气孔(2)与节流槽(3)交界处形成节流面(F11),以供气孔(2)直径为底圆,气膜(5)厚度为高的圆柱面形成节流面(F12),气体流动过程中在节流面(F11)和(F12)处发生第一次节流作用,节流槽(3)和均压槽(4)相连通,以均压槽(4)外径为底圆,气膜(5)厚度为高的圆柱面形成节流面(F2),气体流动过程中在节流面(F2)处发生第二次节流作用。",
    }
    :param rows:
    :param start:
    :param solr_select_url:
    :return:
    """
    params = {
        "start": start,
        "rows": rows,
        "indent": "on",
        "wt": "json",
        "q": "type:2",
        "fl": "pubId, zhTitle, cabstract",
    }

    resp = requests.get(solr_select_url, params)
    docs = resp.json()['response']['docs']
    return docs


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
        for context in dict_list:
            # add 需要知道是什么操作
            segment_list.append(
                {
                    "add": {
                        "doc": context
                    }
                }
            )

    return segment_list


def update_to_solr(solr_update_url, dict_list):
    """
    {
        "add": {
            "doc": {.......}
        },
        "add": {
            "doc": {.......}
        },
       ............. and so on.
    }

    :param solr_update_url:
    :param dict_list:
    :return:
    """

    # 需要有提交参数
    update_params = {
        "boost": 1.0,
        "commitWithin": 100,
        "overwrite": "true",
        "wt": "json",
        "indent": "on",
    }

    headers = {
        "Content-type": "application/json"
    }

    # 拼接
    data = str(dict_list).replace("[", "{").replace("]", "").replace("{'add", "'add").replace("},", ",")
    # print(data)

    r = requests.post(solr_update_url, data=data.encode('utf-8'), params=update_params, headers=headers)
    # 实现 ?: ["responseHeader"]["status"] == 0 and "update solr success" or "update solr fail"
    return r.json()


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


SOLR_SELECT_URL = "http://192.168.15.13:8091/solr/solr_cores_high_new_tech/select?"
SOLR_UPDATE_URL = "http://192.168.15.13:8091/solr/collection1/update?"


def task(start, rows):
    # 获取solr中数据

    json_docs = get_solr_data(SOLR_SELECT_URL, start, rows)

    # 处理solr中数据
    segment_list = handle_solr_data(json_docs)

    # 保存到 solr

    resp = update_to_solr(SOLR_UPDATE_URL, segment_list)
    print("start:%d , rows:%d , response:%s" % (start, rows, resp))


def main():
    # 分配 task
    params = {
        "indent": "on",
        "wt": "json",
        "q": "type:2",
        "fl": "pubId",
    }
    resp = requests.get(SOLR_SELECT_URL, params)
    num_found = resp.json()['response']['numFound']

    rows = 2000
    # tasks = []
    for _ in range(100):
        start = 0
        while start < num_found:
            # tasks.append(task(start, rows))
            task(start, rows)
            start += rows

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()


if __name__ == '__main__':
    main()
