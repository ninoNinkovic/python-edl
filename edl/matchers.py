import re
import sys
import timecode
from .effects import Timewarp, Cut, Dissolve, Wipe, Key
from .event import Event


class Matcher(object):
    """No documentation for this class yet.
    """

    def __init__(self, with_regex):
        self.regex = with_regex

    def matches(self, line):
        return re.match(self.regex, line)

    def apply(self, stack, line):
        sys.stderr.write("Skipping:" + line)
        return True


class TitleMatcher(Matcher):
    """Matches the EDL Title attribute
    """
    def __init__(self):
        Matcher.__init__(self, 'TITLE: (.+)')

    def apply(self, stack, line):
        m = re.search(self.regex, line)
        try:
            stack.title = m.group(1).strip()
            return True
        except (IndexError, AttributeError):
            return False


class CommentMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self):
        Matcher.__init__(self, '\*\s*(.+)')

    def apply(self, stack, line):
        #print line
        m = re.search(self.regex, line)
        if m:
            # TODO: Handle comments that are not tied to an event
            if len(stack) > 0:
                stack[-1].comments.append("* " + m.group(1))
                mo = re.search('\*\s+FROM\s+CLIP\s+NAME:\s+(.+)', line)
                if mo:
                    stack[-1].clip_name = mo.group(1).strip()
                return True
        else:
            return False


class FallbackMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self):
        Matcher.__init__(self, '/^(\w)(.+)/')

    def apply(self, stack, line):
        return True


class NameMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self):
        # TODO: shouldn't it be '\*\s*FROM\s+CLIP\s+NAME:(\s+)(.+)' as above,
        #       add a test for this
        Matcher.__init__(self, '\*\s*FROM CLIP NAME:(\s+)(.+)')

    def apply(self, stack, line):
        m = re.search(self.regex, line)
        if m and len(stack) > 0:
            stack[-1].clip_name = m.group(2).strip()
            return True
        else:
            return False


class SourceMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self):
        Matcher.__init__(self, '\*\s*SOURCE FILE:(\s+)(.+)')

    def apply(self, stack, line):
        m = re.search(self.regex, line)

        if m and len(stack) > 0:
            stack[-1].source_file = m.group(2).strip()
            return True
        else:
            return False


class EffectMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self):
        Matcher.__init__(self, 'EFFECTS NAME IS(\s+)(.+)')

    def apply(self, stack, line):
        m = re.search(self.regex, line)
        if m:
            stack[-1].transition.effect = m.group(2).strip()
            return True
        else:
            return False


class TimewarpMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self, fps):
        self.fps = fps
        self.regexp = 'M2\s+(\w+)\s+(\-*\d+\.\d+)\s+(\d+:\d+:\d+[\:\;]\d+)'
        #self.regexp = 'M2\s+(\S+)\s+(\S+)\s+(\S+)'
        Matcher.__init__(self, self.regexp)

    def apply(self, stack, line):
        m = re.search(self.regexp, line)
        if m:
            stack[-1].timewarp = \
                Timewarp(m.group(1), m.group(2), m.group(3), self.fps)
            if float(m.group(2)) < 0:
                stack[-1].timewarp.reverse = True
            return True
        else:
            return False


class EventMatcher(Matcher):
    """No documentation for this class yet.
    """

    def __init__(self, fps):
        regexp = re.compile(
            r"(?P<num>\d+)\s+"
            r"(?P<reel>\S+)\s+"
            r"(?P<track>\S+)\s+"
            r"(?P<tr_code>\S+)\s+"
            r"(?P<aux>\S*)\s+"
            r"(?P<src_in>\d{1,2}:\d{1,2}:\d{1,2}[:;]\d{1,3})\s+"
            r"(?P<src_out>\d{1,2}:\d{1,2}:\d{1,2}[:;]\d{1,3})\s+"
            r"(?P<rec_in>\d{1,2}:\d{1,2}:\d{1,2}[:;]\d{1,3})\s+"
            r"(?P<rec_out>\d{1,2}:\d{1,2}:\d{1,2}[:;]\d{1,3})")
        Matcher.__init__(self, regexp)
        self.fps = fps
        self._keys = ['num', 'reel', 'track', 'tr_code', 'aux', 'src_start_tc',
                      'src_end_tc', 'rec_start_tc', 'rec_end_tc']

    @classmethod
    def stripper(cls, in_string):
        return in_string.strip()

    def apply(self, stack, line):
        m = re.search(self.regex, line.strip())
        if m:
            matches = m.groups()
            values = map(self.stripper, matches)
            evt = Event(dict(zip(self._keys, values)))
            t = evt.tr_code
            if t == 'C':
                if len(stack) > 0:
                    stack[-1].next_event = evt
                evt.transition = Cut()
            elif t == 'D':
                evt.transition = Dissolve()
            elif re.match('W\d+', t):
                evt.transition = Wipe()
            elif t == 'K':
                evt.transition = Key()
            else:
                evt.transition = None
            evt.src_start_tc = timecode.Timecode(self.fps, evt.src_start_tc)
            evt.src_end_tc = timecode.Timecode(self.fps, evt.src_end_tc)
            evt.rec_start_tc = timecode.Timecode(self.fps, evt.rec_start_tc)
            evt.rec_end_tc = timecode.Timecode(self.fps, evt.rec_end_tc)
            stack.append(evt)
            return True
        else:
            return False
