from tests_unittest.app_test import *


class TestUser(MyTest):

    def setUp(self):
        self.auditorium_num = "10"
        self.max_people_count = "48"

        self.data = {"auditorium_num": self.auditorium_num, "max_people_count": self.max_people_count, }
        self.header = {"Content-Type": "application/json", }

    def test1_post_auditorium(self):
        resp = self.client.post("http://localhost:5000/auditorium", headers=self.header, data=json.dumps(self.data))
        self.assertEqual(200, resp.status_code)

    def test2_get_auditoriums(self):
        resp = self.client.get("http://localhost:5000/auditorium")
        self.assertEqual(200, resp.status_code)

    def test3_get_auditorium(self):
        resp = self.client.get("http://localhost:5000/auditorium/" + self.auditorium_num)
        self.assertEqual(200, resp.status_code)

    def test4_put_auditorium(self):
        resp = self.client.put("http://localhost:5000/auditorium/" + self.auditorium_num, headers=self.header,
                               data=json.dumps({"max_people_count": "100"}))
        self.assertEqual(200, resp.status_code)

    def test9_delete_auditorium(self):
        resp = self.client.delete("http://localhost:5000/auditorium/" + self.auditorium_num)
        self.assertEqual(200, resp.status_code)