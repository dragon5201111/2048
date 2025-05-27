import time


class Util:
    @staticmethod
    def lerp(t, start_list, end_list):
        return tuple(s + (e - s) * t for s, e in zip(start_list, end_list))


class Interpolator:
    def __init__(self):
        self.is_interpolating = False
        self.start_time = None
        self.duration = None
        self.start_pos = None
        self.end_pos = None

    def reset(self, start_pos, end_pos, duration):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.start_time = time.time()
        self.is_interpolating = True

    def is_finished(self):
        return not self.is_interpolating

    def get_position(self):
        if self.is_finished():
            return self.end_pos

        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time >= self.duration:
            self.is_interpolating = False

        t = min(elapsed_time / self.duration, 1.0)
        return Util.lerp(t, self.start_pos, self.end_pos)
