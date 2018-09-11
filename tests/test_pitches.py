import unittest
from app.models import Pitches, User
from flask_login import current_user
from app import db

class TestPitches(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username='Ras', pass_key='Sword', email='ras@sword.com')
        self.new_pitch = Pitches(title = 'Make it', pitch='We shall finish what we started'
                                 ,category='motivational')

    def tearDown(self):
        Pitches.query.delete()
        User.query.delete()

    def test_instance_variables(self):
        self.assertEquals(self.new_pitch.title,'Make it')
        self.assertEquals(self.new_pitch.category,'motivational')
        self.assertEquals(self.new_pitch.pitch,'We shall finish what we started')

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitches.query.all()) > 0)

    def test_get_pitchs(self):
        self.new_pitch.save_pitch()
        got_pitchess = Pitches.get_pitchs(12345)
        self.assertTrue(len(got_pitchess) == 0)