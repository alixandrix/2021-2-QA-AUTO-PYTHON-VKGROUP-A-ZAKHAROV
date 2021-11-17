from models.model import First, Second, Third


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
            type_req = 'rubbish'
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
