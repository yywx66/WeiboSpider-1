import unittest


class TestWeiboSpider(unittest.TestCase):
    # 这单元测试写得我很尴尬...
    def test_get_login_info(self):
        from db import login_info
        infos = login_info.get_login_info()
        self.assertEquals(len(infos), 8)

    def test_login(self):
        import random
        from wblogin.login import get_session
        from db.login_info import get_login_info
        infos = get_login_info()
        info = random.choice(infos)
        sc = get_session(info.name, info.password)

        if sc:
            print('登陆成功')
        else:
            raise Exception('登录失败')

    def test_freeze_account(self):
        from db import login_info
        login_info.freeze_account('18708103033')
        infos = login_info.get_login_info()
        for info in infos:
            if info[0] == '18708103033':
                self.assertEqual(info.enable, 0)

    def test_delete_cookies(self):
        from db.redis_db import Cookies
        r = Cookies.delete_cookies('18708103033')
        self.assertEqual(r, True)

    def test_page_get(self):
        from page_get import basic
        test_url = 'http://weibo.com/p/1005051764222885/info?mod=pedit_more'
        text = basic.get_page(test_url)
        self.assertIn('深扒娱乐热点', text)

    def test_parse_user_info(self):
        from page_parse.user import person, public
        from page_get.user import get_user_detail
        with open('./tests/writer.html') as f:
            cont = f.read()
        user = person.get_detail(cont)
        user.verify_type = public.get_verifytype(cont)
        self.assertEqual(user.verify_type, 1)
        self.assertEqual(user.description, '韩寒')
        with open('./tests/person.html') as f:
            cont = f.read()
        user = get_user_detail('222333312', cont)
        self.assertEqual(user.follows_num, 539)

    def test_get_url_from_web(self):
        from page_get import user as user_get
        normal_user = user_get.get_profile('1195908387')
        self.assertEqual(normal_user.name, '日_推')
        writer = user_get.get_profile('1191258123')
        self.assertEqual(writer.description, '韩寒')
        enterprise_user = user_get.get_profile('1839256234')
        self.assertEqual(enterprise_user.level, 36)

    def test_get_fans(self):
        from page_parse.user import public
        with open('./tests/fans.html') as f:
            cont = f.read()
        public.get_fans_or_follows(cont)
        ids, cur_urls = public.get_fans_or_follows(cont)
        self.assertEqual(len(ids), 9)
        self.assertEqual(len(cur_urls), 5)

    def test_bulk_insert_with_duplicates(self):
        from db.seed_ids import insert_seeds
        ids = ['2891529877', '2891529878', '281296709']
        insert_seeds(ids)

    def test_crawl_person_infos(self):
        from tasks.user import crawl_person_infos
        crawl_person_infos('2041028560')

if __name__ == '__main__':
    unittest.main()