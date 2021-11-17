from models.model import *


class MysqlORMBuilder:

    def __init__(self, client):
        self.client = client

    def create_first_table(self, sum_req):
        first_task = First(
            sum_request=sum_req
        )

        self.client.session.add(first_task)
        self.client.session.commit()
        return first_task

    def create_second_table(self, type_req, sum_req):
        if len(type_req) > 20:
            type_req = 'strange method'
        second_task = Second(
            type_request=type_req,
            sum_request=sum_req
        )
        self.client.session.add(second_task)
        self.client.session.commit()
        return second_task

    def create_third_table(self, url, sum_req):
        third_task = Third(
            url=url,
            sum_request=sum_req
        )
        self.client.session.add(third_task)
        self.client.session.commit()
        return third_task

    def create_fourth_table(self, url, status, size, ip_addr):
        fourth_task = Fourth(
            url=url,
            status=status,
            size=size,
            ip_addr=ip_addr
        )
        self.client.session.add(fourth_task)
        self.client.session.commit()
        return fourth_task

    def create_fifth_table(self, ip_addr, sum_req):
        fifth_task = Fifth(
            ip_addr=ip_addr,
            sum_request=sum_req
        )
        self.client.session.add(fifth_task)
        self.client.session.commit()
        return fifth_task
