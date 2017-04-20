import timecode


class Effect(object):
    """No documentation for this class yet.
    """

    def __init__(self):
        pass


class Cut(Effect):
    """No documentation for this class yet.
    """

    def __init__(self):
        Effect.__init__(self)


class Wipe(Effect):
    """No documentation for this class yet.
    """

    def __init__(self):
        Effect.__init__(self)


class Dissolve(Effect):
    """No documentation for this class yet.
    """

    def __init__(self):
        Effect.__init__(self)


class Key(Effect):
    """No documentation for this class yet.
    """

    def __init__(self):
        Effect.__init__(self)


class Timewarp(object):
    """No documentation for this class yet.
    """

    def __init__(self, reel, warp_fps, tc, fps):
        self.reverse = False
        self.reel = reel
        self.fps = fps
        self.warp_fps = float(warp_fps)
        self.timecode = timecode.Timecode(fps, tc)
        self.timecode_warped = timecode.Timecode(abs(self.warp_fps), tc)

    def to_string(self):
        """the string representation of this Timewarp instance
        """
        return 'M2   %(reel)-8s %(warp_fps)s %(timecode)32s ' % {
            'reel': self.reel,
            'warp_fps': self.warp_fps,
            'timecode': self.timecode
        }
