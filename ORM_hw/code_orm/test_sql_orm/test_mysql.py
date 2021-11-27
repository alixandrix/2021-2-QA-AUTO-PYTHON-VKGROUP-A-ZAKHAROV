from test_sql_orm.funcs import line_count, count_response, popular_url, client_error, server_error
from test_sql_orm.base import MysqlBase
from models.model import First, Second, Third, Fourth, Fifth


class TestMysqlFirst(MysqlBase):

    def prepare(self, log_file):
        self.first_task = self.mysql_builder.create_first_table(line_count(log_file))

    def test_first(self):
        first = self.get_task(First)
        assert len(first) == 1


class TestMysqlSecond(MysqlBase):

    def prepare(self, log_file):
        my_dict = count_response(log_file)
        for k in my_dict.keys():
            self.second_task = self.mysql_builder.create_second_table(k, my_dict[k])

    def test_second(self):
        second = self.get_task(Second)
        assert len(second) == 5


class TestMysqlThird(MysqlBase):

    def prepare(self, log_file):
        dict = popular_url(log_file)
        for k in dict.keys():
            self.third_task = self.mysql_builder.create_third_table(k, dict[k])

    def test_third(self):
        third = self.get_task(Third)
        assert len(third) == 10


class TestMysqlFourth(MysqlBase):

    def prepare(self, log_file):
        dict = client_error(log_file)
        for k in dict.keys():
            self.fourth_task = self.mysql_builder.create_fourth_table(k, dict[k][0], dict[k][1], dict[k][2])

    def test_fourth(self):
        fourth = self.get_task(Fourth)
        assert len(fourth) == 5

class TestMysqlFifth(MysqlBase):

    def prepare(self, log_file):
        dict = server_error(log_file)
        for k in dict.keys():
            self.fifth_task = self.mysql_builder.create_fifth_table(k, dict[k])

    def test_fifth(self):
        fifth = self.get_task(Fifth)
        assert len(fifth) == 5
