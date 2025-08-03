from copy import deepcopy

class BeatmapDataException(Exception):
    def __init__(self, msg=''):
        super().__init__(msg)

class OptionNameException(BeatmapDataException):
    def __init__(self, msg=''):
        super().__init__(msg)

class OptionValueException(BeatmapDataException):
    def __init__(self, msg=''):
        super().__init__(msg)

# ===== Option ===== #

class Option:
    @staticmethod
    def closedrange(lower, upper):
        return {
            'lower': lower,
            'upper': upper
        }

    def __init__(self, value, inst, bound=None):
        self.value = value
        self.inst = inst # 타입
        self.bound = bound # 범위
    
    def validity(self, value):
        if isinstance(value, self.inst):
            if self.bound is None:
                return True
            else:
                if self.inst == str:
                    return value in self.bound
                else:
                    return self.bound['lower'] <= value <= self.bound['upper']
        else:
            return False

# ===== BeatmapData ===== #

class BeatmapData:
    def setOption(self, key, value):
        if key in self.data:
            if self.data[key].validity(value):
                self.data[key].value = value
                return value
            else:
                raise OptionValueException()
        else:
            raise OptionNameException()
    
    def getOption(self, key):
        if key in self.data:
            return self.data[key].value
        else:
            raise OptionNameException()
        
class BDgeneral(BeatmapData):
    options = dict(
        AudioFilename = Option(
            value = '', 
            inst = str
        ),
        AudioLeadIn = Option(
            value = 0,
            inst = int
        ),
        PreviewTime = Option(
            value = -1,
            inst = int
        ),
        Countdown = Option(
            value = 1, 
            inst = int, 
            bound = Option.closedrange(0, 3)
        ),
        SampleSet = Option(
            value = 'Normal', 
            inst = str,
            bound = ['Normal', 'Soft', 'Drum']
        ),
        StackLeniency = Option(
            value = 0.7,
            inst = float,
            bound = Option.closedrange(0, 1)
        ),
        Mode = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 3)
        ),
        LetterboxInBreaks = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        UseSkinSprites = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        OverlayPosition = Option(
            value = 'NoChange',
            inst = str,
            bound = ['NoChange', 'Below', 'Above']
        ),
        SkinPreference = Option(
            value = '',
            inst = str
        ),
        EpilepsyWarning = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        CountdownOffset = Option(
            value = 0,
            inst = int
        ),
        SpecialStyle = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        WidescreenStoryboard = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        SamplesMatchPlaybackRate = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 1)
        )
    )

    def __init__(self):
        self.data = deepcopy(BDgeneral.options)

class BDeditor(BeatmapData):
    options = dict(
        Bookmarks = Option(
            value = [],
            inst = list
        ),
        DistanceSpacing = Option(
            value = 1.0,
            inst = float
        ),
        BeatDivisor = Option(
            value = 4,
            inst = int
        ),
        GridSize = Option(
            value = 16,
            inst = int
        ),
        TimelineZoom = Option(
            value = 1,
            inst = int
        )
    )

    def __init__(self):
        self.data = deepcopy(BDeditor.options)

class BDmetadata(BeatmapData):
    options = dict(
        Title = Option(
            value = '',
            inst = str
        ),
        TitleUnicode = Option(
            value = '',
            inst = str
        ),
        Artist = Option(
            value = '',
            inst = str
        ),
        ArtistUnicode = Option(
            value = '',
            inst = str
        ),
        Creator = Option(
            value = '',
            inst = str
        ),
        Version = Option(
            value = '',
            inst = str
        ),
        Source = Option(
            value = '',
            inst = str
        ),
        Tags = Option(
            value = '',
            inst = list
        ),
        BeatmapID = Option(
            value = '',
            inst = int
        ),
        BeatmapSetID = Option(
            value = '',
            inst = int
        )
    )

    def __init__(self):
        self.data = deepcopy(BDmetadata.options)

class BDdifficulty(BeatmapData):
    options = dict(
        HPDrainRate = Option(
            value = 5.0,
            inst = float,
            bound = Option.closedrange(0, 10)
        ),
        CircleSize = Option(
            value = 5.0,
            inst = float,
            bound = Option.closedrange(0, 10)
        ),
        OverallDifficulty = Option(
            value = 5.0,
            inst = float,
            bound = Option.closedrange(0, 10)
        ),
        ApproachRate = Option(
            value = 5.0,
            inst = float,
            bound = Option.closedrange(0, 10)
        ),
        SliderMultiplier = Option(
            value = 1.4,
            inst = float
        ),
        SliderTickRate = Option(
            value = 1.0,
            inst = float
        )
    )

    def __init__(self):
        self.data = deepcopy(BDdifficulty.options)

class BDevents(BeatmapData):
    pass

class BDtimingpoints(BeatmapData):
    options = dict(
        Time = Option(
            value = 0,
            inst = int
        ), # 시작 지점
        BeatLength = Option(
            value = 0.0,
            inst = float
        ),
        Meter = Option(
            value = 5.0,
            inst = int
        ), # 박자
        SampleSet = Option(
            value = 0,
            inst = int,
            bound = Option.closedrange(0, 3)
        ), # 히트사운드 종류
        SampleIndex = Option(
            value = 0,
            inst = int
        ), # 커스텀 히트사운드셋 인덱스 (0 -> osu! default)
        Volume = Option(
            value = 100,
            inst = int,
            bound = Option.closedrange(0, 100)
        ), # 히트사운드 볼륨
        Uninherited = Option(
            value = 1,
            inst = int,
            bound = Option.closedrange(0, 1)
        ),
        Effects = Option(
            value = 0,
            inst = int
        )
    )

    def __init__(self):
        self.data = deepcopy(BDtimingpoints.options)

    def setBPM(self, bpm):
        self.setOption('BeatLength', (60000 / bpm))

    def getBPM(self):
        return (60000 / self.getOption('BeatLength'))
    
class BDcolours(BeatmapData):
    pass

class Note(BeatmapData):
    @staticmethod
    def calcX(linetuple):
        line_num, key_count = linetuple
        return int((line_num - .5) * (512 / key_count))

    def __init__(self, linetuple, spec, start, end=None):
        # linetuple = (line_number, key_count)
        self.data = dict(
            X = Option(
                value = Note.calcX(linetuple),
                inst = int
            ),
            Y = Option(
                value = 192,
                inst = int
            ),
            Time = Option(
                value = start,
                inst = int
            ),
            Type = Option(
                value = spec,
                inst = int
            ),
            HitSound = Option(
                value = 0,
                inst = int
            )
        )
        if not(end is None):
            self.data['EndTime'] = Option(
                value = end,
                inst = int
            )

class CircleNote(Note):
    def __init__(self, linetuple, start):
        super().__init__(linetuple, 1, start)

class HoldNote(Note):
    def __init__(self, linetuple, start, end):
        super().__init__(linetuple, 128, start, end)

class BDhitobjects:
    def __init__(self):
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

# ===== Beatmap ===== #

class Beatmap:
    def __init__(self):
        self.General = BDgeneral()
        self.Editor = BDeditor()
        self.Metadata = BDmetadata()
        self.Difficulty = BDdifficulty()
        self.Events = BDevents()
        self.TimingPoints = BDtimingpoints()
        self.Colours = BDcolours()
        self.HitObjects = BDhitobjects()

    def compile(self):
        result = 'osu file format v14\n'
        result += '\n[General]\n'
        for key in self.General.data:
            result += f'{key}: {self.General.getOption(key)}\n'
        result += '\n[Editor]\n'
        for key in self.Editor.data:
            result += f'{key}: {self.Editor.getOption(key)}\n'
        result += '\n[Metadata]\n'
        for key in self.Metadata.data:
            result += f'{key}: {self.Metadata.getOption(key)}\n'
        result += '\n[Difficulty]\n'
        for key in self.Difficulty.data:
            result += f'{key}: {self.Difficulty.getOption(key)}\n'
        result += '\n[Events]\n'
        result += '\n[TimingPoints]\n'
        for key in self.TimingPoints.data:
            result += f'{self.TimingPoints.getOption(key)}, '
        result = result[:-2]
        result += '\n'
        result += '\n[Colours]\n'
        result += '\n'
        result += '\n[HitObjects]\n'
        for note in self.HitObjects.notes:
            for key in note.data:
                result += f'{note.getOption(key)}, '
            result = result[:-2]
            result += '\n'
        return result

import random as rd

class JackmapGenerator4K:
    def __init__(self, n, freq, d):

        # 마디 수
        self.n = n
        # 동치 비중
        self.freq = freq

        # 연타 수 상한선
        self.d = d

    def get_max_freq(self):
        r = 0
        for i in range(1, 4):
            if self.freq[r] < self.freq[i]:
                r = i
        return r

    def get_num_chords(self):
        result = [*map(lambda x: int(self.n*x*.01), self.freq)]
        result[self.get_max_freq()] += (self.n - sum(result))
        return result

    def get_order(self):
        num_chords = self.get_num_chords()
        result = []
        for c in range(len(num_chords)):
            result += [ c ]*num_chords[c]
        rd.shuffle(result)
        return result

    def create_jack(self):
        JACKS = [
            [0b0001, 0b0010, 0b0100, 0b1000],
            [0b0011, 0b0101, 0b0110, 0b1001, 0b1010, 0b1100],
            [0b0111, 0b1011, 0b1101, 0b1110],
            [0b1111]
        ]

        result = []
        order = self.get_order()
        for i in range(self.n):
            c = order[i]
            if i < self.d:
                result.append(rd.choice(JACKS[c]))
            else:
                s = result[i-self.d]
                for j in range(i-self.d+1, i):
                    s &= result[j]
                cand = [*filter(lambda x: not(s & x), JACKS[c])]
                if len(cand):
                    result.append(rd.choice(cand))
                else:
                    return self.create_jack()
        return result
    
    @staticmethod
    def export_jack(bm, jack):
        for i in range(len(jack)):
            md = list(bin(jack[i])[2:].zfill(4))
            for k in range(4):
                if bool(int(md[k])):
                    note = CircleNote((k+1, 4), int(round(bm.TimingPoints.getOption('Time')+i*bm.TimingPoints.getOption('BeatLength')*.25)))
                    bm.HitObjects.addNote(note)
        return bm.compile()

def visualize(jack):
    for v in jack:
        print(''.join(map(lambda t: [' ', '='][int(t)], list(bin(v)[2:].zfill(4)))))

bm = Beatmap()
bm.TimingPoints.setBPM(100)
bm.TimingPoints.setOption('Time', 0)
jg = JackmapGenerator4K(50, (0, 65, 25, 10), 3)

print(JackmapGenerator4K.export_jack(bm, jg.create_jack()))

