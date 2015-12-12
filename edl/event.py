from .effects import Cut, Timewarp


class Event(object):
    """Represents an edit event (or, more specifically, an EDL line denoting a
    clip being part of an EDL event)
    """

    def __init__(self, options):
        """Initialisation function with options:
        """
        self.comments = []
        self.timewarp = None
        self.next_event = None
        self.track = None
        self.clip_name = None
        self.source_file = None
        self.transition = None
        self.aux = None
        self.reel = None
        self.rec_end_tc = None
        self.rec_start_tc = None
        self.src_end_tc = None
        self.src_start_tc = None
        self.num = None
        self.tr_code = None

        # TODO: This is absolutely wrong and not safe. Please validate the
        #       incoming values, before adopting them as instance variables
        #       and instance methods
        for o in options:
            self.__dict__[o] = options[o]

    # def __repr__(self):
    #     v = ["(\n"]
    #     for k in self.__dict__:
    #         v.append("    %s=%s,\n" % (k, self.__dict__[k]))
    #     v.append(")")
    #     return ''.join(v)

    def to_string(self):
        """Human Readable string representation of edl event.

        Returns the string representation of this Event which is suitable
        to be written to a file to gather back the EDL itself.
        """
        effect = ''
        if self.transition:
            try:
                effect = 'EFFECTS NAME IS %s\n' % self.transition.effect
            except AttributeError:
                pass

        s = "%(num)-6s %(reel)-32s %(track)-5s %(tr_code)-3s %(aux)-4s " \
            "%(src_start_tc)s %(src_end_tc)s %(rec_start_tc)s " \
            "%(rec_end_tc)s\n" \
            "%(effect)s" \
            "%(notes)s" \
            "%(timewarp)s" % {
                'num': self.num if self.num else '',
                'reel': self.reel if self.reel else '',
                'track': self.track if self.track else '',
                'aux': self.aux if self.aux else '',
                'tr_code': self.tr_code if self.tr_code else '',
                'src_start_tc': self.src_start_tc,
                'src_end_tc': self.src_end_tc,
                'rec_start_tc': self.rec_start_tc,
                'rec_end_tc': self.rec_end_tc,
                'effect': effect,
                'notes': '%s\n' % '\n'.join(self.comments)
                if self.comments else '',
                'timewarp': '%s\n' % self.timewarp.to_string()
                if self.has_timewarp() else ''}

        return s

    def get_comments(self):
        """Return comments array
        """
        return self.comments

    def outgoing_transition_duration(self):
        """TBC
        """
        if self.next_event:
            return self.next_event.incoming_transition_duration()
        else:
            return 0

    def reverse(self):
        """Returns true if clip is timewarp reversed
        """
        return self.timewarp and self.timewarp.reverse

    def copy_properties_to(self, event):
        """Copy event properties to another existing event object
        """
        for k in self.__dict__:
            event.__dict__[k] = self.__dict__[k]
        return event

    def has_transition(self):
        """Returns true if clip if clip uses a transition and not a Cut
        """
        return not isinstance(self.transition, Cut)

    def incoming_transition_duration(self):
        """Returns incoming transition duration in frames, returns 0 if no
        transition set
        """
        d = 0
        if not isinstance(self.transition, Cut):
            d = int(self.aux)
        return d

    def ends_with_transition(self):
        """Returns true if the clip ends with a transition (if the next clip
        starts with a transition)
        """
        if self.next_event:
            return self.next_event.has_transition()
        else:
            return False

    def has_timewarp(self):
        """Returns true if the clip has a timewarp (speed ramp, motion memory,
        you name it)
        """
        if isinstance(self.timewarp, Timewarp):
            return True
        else:
            return False

    def black(self):
        """Returns true if event is black slug
        """
        return self.reel == "BL"

    def rec_length(self):
        """Returns record length of event in frames before transition
        """
        return self.rec_end_tc.frames - self.rec_start_tc.frames

    def rec_length_with_transition(self):
        """Returns record length of event in frames including transition
        """
        return self.rec_length() + self.outgoing_transition_duration()

    def src_length(self):
        """Returns source length of event in frames before transition
        """
        return self.src_end_tc.frames - self.src_start_tc.frames

    def capture_from_tc(self):
        raise NotImplementedError

    def capture_to_and_including_tc(self):
        raise NotImplementedError

    def capture_to_tc(self):
        raise NotImplementedError

    def speed(self):
        raise NotImplementedError

    def generator(self):
        raise NotImplementedError

    def get_clip_name(self):
        return self.clip_name

    def get_reel(self):
        return self.reel

    def event_number(self):
        return self.num

    def get_track(self):
        return self.track

    def get_tr_code(self):
        return self.tr_code

    def get_aux(self):
        return self.aux
