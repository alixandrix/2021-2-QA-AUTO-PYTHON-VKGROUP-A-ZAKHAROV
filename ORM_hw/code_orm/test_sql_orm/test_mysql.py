from test_sql_orm.funcs import *
from test_sql_orm.base import MysqlBase
from models.model import First, Second, Third


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

    def prepare(self, log_file='access.log'):
        dict = popular_url(log_file)
        for k in dict.keys():
            self.third_task = self.mysql_builder.create_third_table(k, dict[k])

    def test_third(self):
        third = self.get_task(Third)
        assert len(third) == 10

"""class TestMysqlDelete(TestMysqlCreate):

    # inherits prepare method from TestMysqlCreate

    def test(self):
        # tests should be independent, so
        # we need to delete data created by this test
        student_to_delete = self.students[0].id
        self.mysql.session.query(Student).filter_by(id=student_to_delete).delete()

        # and get data by concrete prepod_id, created in current test
        assert len(self.get_students(prepod_id=self.prepod.id)) == 9

        # this code is wrong, we can't delete all students,
        # cause there can be data from other tests running in parallel
        self.mysql.session.query(Student).delete()
        assert len(self.get_students()) == 0"""
