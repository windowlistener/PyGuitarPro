import warnings

import pytest

import guitarpro as gp


def test_hashable():
    song = gp.Song()
    hash(song)

    coda = gp.DirectionSign('Coda')
    segno = gp.DirectionSign('Segno')
    assert coda != segno
    assert hash(coda) != hash(segno)


@pytest.mark.parametrize('value', [1, 2, 4, 8, 16, 32, 64])
@pytest.mark.parametrize('isDotted', [False, True])
@pytest.mark.parametrize('tuplet', [gp.Tuplet(1, 1), gp.Tuplet(3, 2)])
def test_duration(value, isDotted, tuplet):
    dur = gp.Duration(value, isDotted=isDotted, tuplet=tuplet)
    time = dur.time
    new_dur = gp.Duration.fromTime(time)
    assert isinstance(new_dur.value, int)
    assert time == new_dur.time


def test_double_dot_warning(recwarn):
    warnings.simplefilter('always')
    d = gp.Duration()
    assert len(recwarn) == 0
    with pytest.deprecated_call():
        d.isDoubleDotted = True


def test_beat_real_start():
    song = gp.Song()
    measure = song.tracks[0].measures[0]
    voice = measure.voices[0]
    beat = gp.Beat(voice, start=measure.start)
    beat2 = gp.Beat(voice, start=measure.start + beat.duration.time)
    voice.beats.append(beat)
    assert beat.realStart == 0
    assert beat2.realStart == 960
