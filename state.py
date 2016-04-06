from google.appengine.ext import ndb
from state_list import STATE_LIST

K = 32


def get_expected(a, b):
    return 1.0 / (1 + pow(10, (float(b - a) / 400)))


def update_rating(expected, actual, current):
    return round(current + K * (actual - expected))


class State(ndb.Model):
    code = ndb.StringProperty()
    name = ndb.StringProperty()
    score = ndb.FloatProperty(default=0)

    def record_win_against(self, other_state):
        expected = get_expected(self.score, other_state.score)
        self.score = update_rating(expected, 1, self.score)
        return self

    def record_loss_against(self, other_state):
        expected = get_expected(self.score, other_state.score)
        self.score = update_rating(expected, 0, self.score)
        return self

    @staticmethod
    def get_or_create(code):
        assert code in STATE_LIST
        result = State.query(State.code == code).get()
        if not result:
            result = State(code=code, name=STATE_LIST[code])
        return result
