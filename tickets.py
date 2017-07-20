# coding: utf-8
"""命令行火车票查看器


Usage:
    tickets [-gdtkz] <from> <to> <date>
    
    
Options:
    -h, --help      显示帮助菜单
    -g              高铁
    -d              动车
    -t              特快
    -k              快速
    -z              直达
    
    
Example:
    tickets 北京 上海 2017-07-21
     tickets -dg 成都 南京 2017-07-21

"""

from docopt import docopt
from stations import stations
import requests
import json
requests.packages.urllib3.disable_warnings()

def cli():
    """comman-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # print(date, from_station,to_station)

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
    print(url)
    r = requests.get(url, verify=False)
    # print(r.json())
    avaliable_train = r.json()['data']['result']
    optios = {v:k for k, v in stations.items()}
    for i in TrainCollection(avaliable_train, optios).query_train_info():
        print(i)


class TrainCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, avaliable_train, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.avaliable_train = avaliable_train
        self.options = options

    def query_train_info(self):
        info_list = []
        for raw_train in self.avaliable_train:
            data_list = raw_train.split('|')

            #车次
            train_no = data_list[3]
            #始发站
            from_staion_code = data_list[6]
            from_staion_name = self.options[from_staion_code]
            #终点站
            to_station_code = data_list[7]
            to_station_name = self.options[to_station_code]
            #出发时间
            start_time = data_list[8]
            #到达时间
            arive_time = data_list[9]
            #历时
            total_time = data_list[10]
            #特等座
            class_seat = data_list[32] or '--'
            #一等座
            fist_class_seat = data_list[31] or '--'
            #二等座
            second_class_seat = data_list[30] or '--'
            #软卧
            soft_sleep = data_list[29] or '--'
            # 硬卧
            hard_sleep = data_list[28]or '--'
            # 硬座
            hard_seat = data_list[26]or '--'
            # 无座
            no_seat = data_list[23]or '--'

            info = ('车次:{} \t始发站:{}\t终点站:{}\t出发时间:{}\t到达时间:{}\t历时:{}\t特等座:{}\t一等座:{}\t二等座:{}\t软卧:{}\t硬卧:{}\t硬座:{}\t无座:{}\t'.format(train_no,from_staion_name,
                                                                                                      to_station_name, start_time, arive_time,total_time,
                                                                                                           class_seat,fist_class_seat, second_class_seat,
                                                                                                             soft_sleep,hard_sleep,hard_seat,no_seat ))
            list_black=('\n------------------------------------------------------------------------------------------------------------------\n')
            info_list.append(list_black)
            info_list.append(info)
        return info_list





if __name__ == '__main__':
    cli()