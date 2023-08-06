"""This file belongs to project 'LIGHTPARTICLE', See README for more detail."""

#  This is not a standalone executable module.

import platform
import time
import signal  # TODO: ??WIN32
from random import Random
from datetime import datetime
import inspect
import uuid
from settings import version, debug, line, verbose


# ### Maintainer(s): _3083 ###
# 2023-07-28    v0.1 Code Review - 1st.
#                   - Fix typos / builtin names
#                   - Generate usage document
#                   - Rename system signal handler function name


def bl4th3r(level: str, msg: str,
            colorize: object = None if platform.system() == "Windows" else
            True) -> None:
    """
    Helper function for spray log to TERMINAL. (Blocking , NOT thread safe.)
    Without any level filter, just debug/verbose mode to open.
    param:
      - <int> level    message level. (different color for output)
      - <str> msg      content of message.
    """

    __color = [  # TODO: Check color on screen.
        '\033[0m',  # No COLOR (Recover)
        '\033[94m',  # Info      Blue    Lv.1
        '\033[96m',  # Warning   Cyan    Lv.2
        '\033[92m',  # Debug     Green   Lv.3
        '\033[93m',  # Error     Yellow  Lv.4
        '\033[91m'  # Critical  Red     Lv.5
    ]
    __level = ["critical", "info", "error", "warn", "debug"]
    _v = __level.index(level.lower())
    if not debug and _v > 3:
        _v = 3
        level = "warn"
    __tm = datetime.now().__str__().split('.')[0]
    __caller = inspect.stack()[1][3]  # Get caller function name.
    __caller = str(__caller).replace("testcase_", 'Test: ')

    if len(__caller) > 8:
        __caller = __caller[:5] + "..."

    if "_" in __caller:
        __caller = __caller.replace("_", '')

    if len(msg) > line > 0:
        msg = msg[:line] + "..."

    # Level 0 is `critical`, always output!
    if _v <= verbose:
        if colorize:
            try:
                print("%s | %-8s |%s %s %s" % (
                    __tm, __caller,
                    __color[__level.index(level.lower())],
                    msg,
                    __color[0])
                      )
            except ValueError as ex:
                print("%s | bl4th3r | No level named %s" % (level, level))
                print(ex)
        else:
            print("%s | %-8s | %s" % (__tm, __caller, msg))

    if _v == 0:
        raise SystemExit


def generate_ua() -> str:
    """
    User-Agent random picker form useragent.dat file.
    """
    _ua = ""
    _idx = Random().randint(0, 100)
    with open("useragent.dat", "r") as fd:
        try:
            for dataline in fd:
                _idx -= 1
                if _idx == 0:
                    _ua = str(dataline)[:-1]
        except IOError:
            # Failed to load a user-agent string.
            bl4th3r("warn", "Failed to generate User-Agent!")
    bl4th3r("debug", "New UA: " + _ua)
    return _ua


def generate_rid() -> str:
    """
    RFC 4122 - UUID generator in random.
    """
    return str(uuid.uuid4())


def ztime(tm=None, year=1900, month=1, date=1, hour=0, minute=0, second=0, ms=0,
          tz=8, ptz=True) -> str | datetime:
    """
    Get a customized timestamp. (timezone Asia/Shanghai by default)

    """
    if ptz:  # URLENCODED
        time_format = "%04d-%02d-%02dT%02d%%3A%02d%%3A%02d.%03d%%2B%02d00"
    else:
        time_format = "%04d-%02d-%02dT%02d%%3A%02d%%3A%02d.%03d-%02d00"

    if tm is None:  # Get current timestamp in zTime format.
        now = datetime.now()
        return time_format % (
            now.year, now.month, now.day, now.hour,
            now.minute, now.second,
            ((now.microsecond / 1000).__floor__()), tz)
    elif isinstance(tm, str) and len(tm) in [28, 34]:  # zTime to time object.
        # No `parse` module, just string splitter
        if len(tm) == 34:  # Mixin encoded! urllib.parse,decode not work!
            _Y = int(tm[:4])  # 1900, b=0,e=3
            _M = int(tm[5:7])  # 01, b=5
            _D = int(tm[8:10])  # 01, b=8
            _h = int(tm[11:13])
            _m = int(tm[16:18])
            _s = int(tm[21:23])
            _ms = int(tm[24:27])  # .000
        elif len(tm) == 28:
            _Y = int(tm[:4])  # 1900, b=0,e=3
            _M = int(tm[5:7])  # 01, b=5
            _D = int(tm[8:10])  # 01, b=
            _h = int(tm[11:13])
            _m = int(tm[14:16])
            _s = int(tm[17:19])
            _ms = int(tm[20:23])  # .000
        else:
            return time_format % (year, month, date,
                                  hour, month, second, ms, tz)
        return datetime(year=_Y, month=_M, day=_D, hour=_h, minute=_m,
                        second=_s,
                        microsecond=(_ms * 1000 + Random().randint(0, 999))
                        )

    elif isinstance(tm, datetime):
        return time_format % (
            tm.year, tm.month, tm.day, tm.hour,
            tm.minute, tm.second,
            ((tm.microsecond / 1000).__floor__()), tz)
    else:  # Return specific ztime string.
        if (1900 > year or year > 2199) and (
                month not in range(1, 12) and (
                date not in range(1, 31) and (
                hour not in range(0, 24) and (
                minute not in range(0, 59) and (
                second not in range(0, 59) and (
                ms > 999) and (tz not in range(0, 12))))))):
            return ""

        tms = time_format % (year, month, date, hour, month, second, ms, tz)

    return tms


def ztime_before(tms):
    """
    The end_time is last_end_time - 0.001. (...sup
    """
    tm = ztime(tms)

    try:
        _ms = tm.microsecond - 1000
        tm = tm.replace(microsecond=_ms)
    except Exception:
        try:
            bl4th3r("debug", "Last second")
            tm = tm.replace(second=tm.second - 1)
            tm = tm.replace(microsecond=999999)
        except Exception:
            bl4th3r("debug", "Last minute")
            tm = tm.replace(minute=tm.minute - 1)
            tm = tm.replace(second=59)
            tm = tm.replace(microsecond=999999)

    bl4th3r("debug", "last timestamp: " + tms)
    before = ztime(tm)
    bl4th3r("debug", "before: " + before)

    return before


def zlink_exceed(url, tm=None) -> bool:  # TODO: Move this to `utility`???
    """
    Check the attachment url is available or exceed time limit.
    Return check status in bool.

    Parameters:
        url:<str>       The link.
        tm:<list>       Store return value for testcase.
    """
    # File - 1hour, Image - 1Month
    # Fix image link exceed time parse error

    if tm is None:
        tm = []
    _tm = 0
    # Get timestramp in url
    from urllib.parse import urlparse, parse_qs
    _tm = int(parse_qs(qs=str(urlparse(url).query))["e"][0])
    from time import time
    bl4th3r("info", "Time exceed: " + str(_tm))
    if isinstance(tm, list):
        tm.append(_tm)  # For testcase use.
    if _tm >= time().__floor__():
        return True
    else:
        bl4th3r("debug", "Exceed Link: " + url)
        return False


# Filter related.
# FILE_LIST [LINK, NAME, ID, SIZE, HASH, DOWN, TID]

def _filter_keyword(result: list, files: list, keyword) -> int:
    """
    Filter files by search keyword in filename.

    Parameters:
        - result:<list>         # return values.
        - files:<list>          # Old list of files.
        - keyword:<str>         # String of your search.
    """
    if isinstance(keyword, str):
        if isinstance(keyword, list):
            keyword = keyword[0]

        if not isinstance(result, list):
            result = []

        for f in files:
            if keyword in str(f[1].split('.')[0]):
                result.append(f)
    else:
        return -1

    return len(result)


def __filter_format(result: list, files: list, fmt) -> int:
    """
    Filter files by format <extension name>.

    Parameters:
        - result:<list>         # return values.
        - files:<list>          # Old list of files.
        - fmt:<list>            # Search format (extension)
    """
    if not isinstance(result, list):
        result = []
    if isinstance(fmt, list):
        for f in files:
            if len(f[1].split('.')) > 1 and f[1].split('.')[-1] in fmt:
                result.append(f)
    else:
        return -1

    return len(result)


def __filter_count(result: list, files: list, mode=-4) -> int:
    """
    Filter files by download counts or file size.

    Parameters:
        - result:<list>         # return values.
        - files:<list>          # Old list of files.
        - mode:<int>            # -4 -> size , -2 -> download counts
    """
    if not isinstance(result, list):
        result = []

    sorted(files, key=lambda x: int(x[mode]))

    files.reverse()

    result += files

    return len(result)


def __entropy(data) -> float:
    """
    Entropy calculator
    """

    import collections
    import math
    ret = 0
    m = len(data)
    dataset = collections.Counter([d for d in data])
    for d in dataset:
        ni = dataset[d]
        pi = ni / float(m)
        ei = pi * (math.log(pi, 2))
        ret += ei
    return ret * -1


def __filter_entropy(result: list, files: list, min=None, max=None,
                     basedir=None, gid=None) -> int:
    """
    Filter files by data entropy

    Parameters:
        - result:<list>         # return values.
        - files:<list>          # Old list of files.
    """
    import json
    from os import listdir
    from os.path import isfile, join

    if not isinstance(result, list):
        result = []

    # TODO: Add parameter `dirname` for replacing hardcode path.
    for f in files:
        _data = [f[1]]
        _topic = f[-1]
        try:
            # Tapic
            with open(
                    str(basedir) + "/static/data/group/" + str(gid) + "/" + str(
                        _topic) + ".json") as fd:
                d = json.loads(fd.read())
                _data.append(str(d))
        except FileNotFoundError:
            bl4th3r("debug", "File missing topic?!")
        # Comment
        try:
            path = str(basedir) + "/static/data/group/" + str(gid) + "/" + str(
                _topic) + "/"

            comments = [f for f in listdir(path) if isfile(join(path, f))]
            for cmt in comments:
                with open(str(basedir) + "/static/data/group/" + str(
                        gid) + "/" + str(_topic) + "/" + cmt, 'r') as fd:
                    d = json.loads(fd.read())
                    _data.append(str(d))
        except FileNotFoundError:
            # bl4th3r("debug", "no comment")
            pass

        e = __entropy(' '.join(_data))

        if min and max:
            if min < e < max:
                f.append(e)
                result.append(f)
        else:
            f.append(e)
            result.append(f)

    sorted(result, key=lambda x: x[-1])
    # result.reverse()

    return len(result)


def value_attachment(files, basedir=None, keyword=None, gid=None, by_size=False,
                     by_trend=False, by_entropy=False):
    """
    Filter valuable attachment.(Under testing, beta)

    Parameters:
        - files:<list>      Download-able object in channel.
        - keyword:<str>     Filter option in default mode. See settings.py.
    """

    for f in files:
        if isinstance(f[2], list):
            f[2] = f[2][0]
    with open("debug_filetask.json", 'w') as fd:
        fd.write(str(files))

    try:
        from settings import filter_mode
        __filter = filter_mode
    except ImportError:
        filter_mode = {"keyword": keyword}
        __filter = filter_mode
        bl4th3r("debug", "Not found any filter settings.")

    __filter_opts = __filter.keys()

    if by_size:
        __filter_opts = {"size", True}
    if by_trend:
        __filter_opts = {"trend", True}

    result_kw = []
    result_fm = []
    result_en = []
    result_sz = []
    result_tr = []

    for opt in __filter_opts:
        match opt.lower():
            case "format":
                __filter_format(result_fm, files, __filter["format"])
            case "entropy":
                if isinstance(__filter["entropy"], bool):
                    __min = None
                    __max = None
                else:
                    try:
                        __min = __filter["entropy"][0]
                        __max = __filter["entropy"][1]
                    except IndexError:
                        __min = None
                        __max = None
                __filter_entropy(
                    result_en, files,
                    basedir=basedir, gid=gid, min=__min, max=__max
                )
            case "size":
                __filter_count(
                    result_sz, files, mode=-4
                )
            case "trend":
                __filter_count(
                    result_tr, files, mode=-2
                )
            case _:
                _filter_keyword(
                    result_kw, files, __filter["keyword"]

                )

    # Synth.
    return set(tuple(e) for e in result_kw[:20]) & set(
        tuple(e) for e in result_fm)


def __signal_handler():
    print("\nQuiting...\n")
    time.sleep(2)
    exit(0)


def quiet_quit():  # TODO: ??WIN32
    signal.signal(signal.SIGINT, __signal_handler)
