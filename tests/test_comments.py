import unittest
from app.models import Pitches,Comments

class TestPitches(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitches(id=12,title = 'Make it', pitch='We shall finish what we started'
                                 ,category='motivational')
        self.new_comment = Comments(comment = "There is no other way")

    def tearDown(self):
        Pitches.query.delete()
        Comments.query.delete()

    def test_instance_variable(self):
        self.assertEquals(self.new_comment.comment, 'There is no other way')

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all()) > 0)

    def test_get_comment(self):
        self.new_comment.save_comment()
        got_coments = Comments.get_comments(12)
        self.assertTrue(len(got_coments) == 0)