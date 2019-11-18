# -*- coding: utf-8 -*-
"""Test: world.py
"""
import unittest
from testutils import print_test_title, validated_testing_withfail
from builder.world import UtilityDict, World
from builder.person import Person


_FILENAME = "world.py"


class UtilityDictTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "UtilityDict class")

    def test_attributes(self):
        tmp = UtilityDict()
        self.assertIsInstance(tmp, UtilityDict)

    def test_setitem(self):
        tmp = UtilityDict()
        tmp.__setitem__("test", "apple")
        self.assertTrue(hasattr(tmp, "test"))
        self.assertEqual(tmp.test, "apple")

class WorldTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print_test_title(_FILENAME, "World class")

    def setUp(self):
        self.taro = Person("Taro", "", 17, "male", "student")

    def test_attributes(self):
        tmp = World()
        self.assertIsInstance(tmp, World)
        self.assertIsInstance(tmp.day, UtilityDict)
        self.assertIsInstance(tmp.item, UtilityDict)
        self.assertIsInstance(tmp.stage, UtilityDict)
        self.assertIsInstance(tmp.time, UtilityDict)
        self.assertIsInstance(tmp.word, UtilityDict)

    @unittest.skip("referenced chapter-test")
    def test_chapter(self):
        pass

    @unittest.skip("referenced episode-test")
    def test_episode(self):
        pass

    @unittest.skip("referenced scene-test")
    def test_scene(self):
        pass

    @unittest.skip("referenced story-test")
    def test_story(self):
        pass

    def test_appendOne(self):
        from builder.stage import Stage
        data = [
                (False, "test", Stage("apple"), UtilityDict(), Stage,),
                (False, "test", ("apple",), UtilityDict(), Stage,),
                ]
        def _checkcode(k, v, dct, dtype):
            tmp = World()
            tmp._appendOne(k, v, dct, dtype)
            self.assertTrue(hasattr(dct, k))
            self.assertIsInstance(dct[k], dtype)
        validated_testing_withfail(self, "appendOne", _checkcode, data)

    @unittest.skip("referenced appendOne test")
    def test_append_chara(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_day(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_item(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_person(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_stage(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_time(self):
        pass

    @unittest.skip("referenced appendOne test")
    def test_append_word(self):
        pass

    def test_setItemsFrom(self):
        from builder.stage import Stage
        data = [
                (False, [("test", "a test"),],),
                (False, [("apple", "an apple"), ("orange", "a orange")],),
                ]
        def _checkcode(data):
            tmp = World()
            tmp._setItemsFrom(data, tmp.append_stage)
            for v in data:
                self.assertTrue(hasattr(tmp.stage, v[0]))
                self.assertIsInstance(tmp.stage[v[0]], Stage)
        validated_testing_withfail(self, "setItemsFrom", _checkcode, data)

    @unittest.skip("referenced setItemsFrom test")
    def test_set_days(self):
        pass

    @unittest.skip("referenced setItemsFrom test")
    def test_set_items(self):
        pass

    @unittest.skip("referenced setItemsFrom test")
    def test_set_persons(self):
        pass

    @unittest.skip("referenced setItemsFrom test")
    def test_set_stages(self):
        pass

    @unittest.skip("referenced setItemsFrom test")
    def test_set_times(self):
        pass

    @unittest.skip("referenced setItemsFrom test")
    def test_set_words(self):
        pass

    @unittest.skip("integration test")
    def test_set_db(self):
        pass

    @unittest.skip("referenced combaction test")
    def test_combine(self):
        pass

    def test_act(self):
        from builder.action import Action, ActType
        data = [
                (False, self.taro, "test",),
                ]
        def _checkcode(subject, outline):
            tmp = World()
            tmp1 = tmp.act(subject, outline)
            self.assertIsInstance(tmp1, Action)
            self.assertEqual(tmp1.subject, subject)
            self.assertEqual(tmp1.outline, outline)
            self.assertEqual(tmp1.act_type, ActType.ACT)
        validated_testing_withfail(self, "act", _checkcode, data)

    @unittest.skip("almost same test_act")
    def test_be(self):
        pass

    @unittest.skip("almost same test_act")
    def test_come(self):
        pass

    @unittest.skip("almost same test_act")
    def test_go(self):
        pass

    @unittest.skip("almost same test_act")
    def test_have(self):
        pass

    @unittest.skip("almost same test_act")
    def test_hear(self):
        pass

    @unittest.skip("almost same test_act")
    def test_look(self):
        pass

    @unittest.skip("almost same test_act")
    def test_move(self):
        pass

    @unittest.skip("almost same test_act")
    def test_talk(self):
        pass

    @unittest.skip("almost same test_act")
    def test_think(self):
        pass

    def test_comment(self):
        from builder.action import TagAction, TagType
        data = [
                (False, "test",),
                ]
        def _checkcode(info):
            tmp = World()
            tmp1 = tmp.comment(info)
            self.assertIsInstance(tmp1, TagAction)
            self.assertEqual(tmp1.info, info)
            self.assertEqual(tmp1.tag_type, TagType.COMMENT)
        validated_testing_withfail(self, "comment", _checkcode, data)

    @unittest.skip("almost same test_comment")
    def test_br(self):
        pass

    @unittest.skip("almost same test_comment")
    def test_hr(self):
        pass

    @unittest.skip("almost same test_comment")
    def test_symbol(self):
        pass

    @unittest.skip("almost same test_comment")
    def test_title(self):
        pass

    @unittest.skip("almost same test_comment")
    def test_layer(self):
        pass

    @unittest.skip("on integration test")
    def test_build(self):
        pass

