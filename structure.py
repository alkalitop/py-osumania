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
        
class BeatmapGeneral(BeatmapData):
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
            value = 3, # 3 = osu!mania
            inst = int,
            bound = Option.closedrange(3, 3)
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
        self.data = deepcopy(BeatmapGeneral.options)

class BeatmapEditor(BeatmapData):
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
        self.data = deepcopy(BeatmapEditor.options)

class BeatmapMetadata(BeatmapData):
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
        self.data = deepcopy(BeatmapMetadata.options)

class BeatmapDifficulty(BeatmapData):
    options = dict(
        HPDrainRate = Option(
            value = 5.0,
            inst = float,
            bound = Option.closedrange(0, 10)
        ),
        CircleSize = Option(
            value = 4, # key count in osu!mania
            inst = int,
            bound = Option.closedrange(4, 18)
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
        self.data = deepcopy(BeatmapDifficulty.options)

class BeatmapEvents(BeatmapData):
    pass

class BeatmapTimingpoints(BeatmapData):
    def __init__(self):
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

class BeatmapDataObject(BeatmapData):
    pass

class Timingpoint(BeatmapDataObject):
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
        self.data = deepcopy(Timingpoint.options)

    def setBPM(self, bpm):
        self.setOption('BeatLength', (60000 / bpm))

    def getBPM(self):
        return (60000 / self.getOption('BeatLength'))


class BeatmapColours(BeatmapData):
    pass

class BeatmapHitobjects(BeatmapData):
    def __init__(self):
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

    def addNotes(self, notes):
        for note in notes:
            self.addNote(note)

class Note(BeatmapDataObject):
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

# ===== Beatmap ===== #

class Beatmap:
    def __init__(self):
        self.General = BeatmapGeneral()
        self.Editor = BeatmapEditor()
        self.Metadata = BeatmapMetadata()
        self.Difficulty = BeatmapDifficulty()
        self.Events = BeatmapEvents()
        self.TimingPoints = BeatmapTimingpoints()
        self.Colours = BeatmapColours()
        self.HitObjects = BeatmapHitobjects()

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
        for point in self.Timingpoints.points:
            for key in point.data:
                result += f'{point.getOption(key)}, '
            result = result[:-2]
            result += '\n'
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

    
