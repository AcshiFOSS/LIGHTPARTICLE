#!/usr/bin/env python3

# This file show some example for usage(s) and develop a new function.
# Running this for testing LIGHTPARTICAL. For more details, refer to
# README file.

# Some values need replace by your own! 
# Some values need replace by your own! 
# Some values need replace by your own! 

import sys
import os
import json
import time
import multiprocessing
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def _null(**kwargs: [None | list]):
    print("Import error occurred before!")
    _no_use = kwargs
    exit(-1)


# Path will be appended in the next line. (Ignore PEP8-E402)
try:
    from utility import quiet_quit, bl4th3r
    from utility import generate_rid as uuid64
    from utility import ztime
    from conn import Connection
    from api import API
    from settings import verbose
except ImportError:  # set _null and exit.
    quiet_quit = _null
    bl4th3r = _null
    uuid64 = _null
    ztime = _null
    Connection = _null
    API = _null
    verbose = None
    pass

# ### Maintainer(s): _3083 ###
# 2023-07-29    Bump v0.1(init), It's works.           
#                 - Make unittest in barely.
#                 - Create usage for testing.
#                 - Add some testcase set for usage.
#
# 2023-07-30    v1.0 Compatibility                     
#                 - Add single testcase mode (-s)
#                 - Fix testcase for functional testing.
#                 - Handle all import error with _null.
#

quiet_quit()  # Add handler C^c ...


def testcase_modules():
    """
    Test core modules loaded.
        - Load modules
    """
    try:
        import api
        import bulk
        import conn
        import daemon
        import error
        import settings
        import utility
    except ImportError:
        print("Missing Core modules...")

    if not os.path.exists("../useragent.dat"):
        print("UserAgent list not available.")


def testcase_env():
    """
    Test running environment.
        - Load settings
        - System and runtime version.
    """
    import settings

    __ver = settings.version
    __serv = settings.serv
    __lib = settings.libmweb

    if verbose >= 5:
        print("Version: %s" % __ver)
        print("Target MWeb Service: %s" % __serv)

        print("Support settings:")
        for x in dir(settings)[9:]:
            print(" + " + x)

        print("Platform: " + os.uname().sysname + ' ' + platform.release())

    assert int(__serv.split('.')[1]) >= 40, "Target service may not supported!"
    assert __lib, "Enhance library inactivated."


def testcase_keys():
    """
    Test Connection object.
        - Load user key file
        - Create connection object instance
    """
    c = Connection(uuid64())

    bl4th3r("debug", "(TS) Conn Obj.: " + c.name)
    bl4th3r("info", "(TS) Cookie: " + c.cookie)
    bl4th3r("info", "(TS) UA: " + c.ua)

    assert len(c.name) == 8, "Wrong name of object"

    assert '=' in c.cookie, "Bad Cookie loaded"
    assert '/' in c.ua, "Bad User-Agent"


def testcase_header():
    """
    Test HTTP request header mockup.
        - Header create
        - X-SIG generation and verify
    """
    __url = "https://127.0.0.1/"
    __time = 1234567890
    __level = "xsec"
    __rid = "12345678-abcd-1234-5678-1234567890abcd"

    __sig = "0d8eb0f7b768709b89d06f4a7f2df2238ed2f0ad"

    c = Connection(uuid64())

    c.request(__url, __level, timestamp=__time, rid=__rid, sig=__sig, step=True)


def testcase_account():
    """
    Get account information which you were logged in.
        - Test user account.
        - Parse user info.
    """
    c = Connection(uuid64())

    r = c.request(API.user(), "xsec")
    print(json.dumps(r[1], indent=2, ensure_ascii=False))

    assert r[0] == 200, "Bad HTTP status"
    assert "user" in r[1], "Wrong Login"


def testcase_group():
    """
    Get user joined groups.
        - Groups API
        - Details parse
    """
    c = Connection(uuid64())

    r = c.request(API.group_list(), "xsec")
    print(json.dumps(r[1], indent=2, ensure_ascii=False))

    assert r[0] in [200, 401], "Bad HTTP status"
    assert "groups" in r[1], "Wrong Login"


def testcase_users():
    """
    Test query user details.
        - Query any others
        - Parse data
    """
    uid = 123456789098765
    from bulk import User
    User(uid).save()
    # In fact, we can initialize user object in manual.
    # That will shirk request count.


def testcase_comment():
    """
    Get comment by topic-id. Get data from online service.
        - Comment class creation.
        - Save comment data on local disk.
    """
    tid = 123456789098765  # Needed
    cid = 123456789098765  # For assertion

    from bulk import Comment
    Comment(tid, 2, basedir=os.getcwd(),
            dirname="TEST_GROUPID-12345678/").save()
    __path = os.getcwd() + "/static/data/TEST_GROUPID-12345678/" + str(
        tid) + "/"
    __file = str(cid) + ".json"
    assert os.path.exists(__path + __file), "Failed to parse comment!"

    import shutil
    shutil.rmtree(__path)


def testcase_topic_load():
    """
    Load topic by topic-id. (From local json file)
        - Load json data.
        - Get jsons.
    """
    qa = 123456789098765
    talk = 123456789098765

    talk_d = "topic-talk.json"
    with open("examples/" + talk_d, 'r') as fd:
        td = fd.read()

    question_d = "topic-question.json"
    with open("examples/" + question_d, 'r') as fd:
        qd = fd.read()

    from bulk import Topic
    Topic(qa, basedir=os.getcwd(), dirname="TEST-1234").question(json.loads(qd))
    Topic(talk, basedir=os.getcwd(), dirname="TEST-1234").talk(json.loads(td))

    __path = os.getcwd() + "/static/data/TEST-1234"
    assert os.path.exists(__path), "Failed to get last comment!"

    import shutil
    shutil.rmtree(__path)


def testcase_topic_load_comment():
    """
    Parse complicated comment data.
        - Nested reply comment
        - Load comment from disk
    """
    tid = 123456789098765
    cid = 123456789098765  # The last one: comment id=19.

    from bulk import Comment
    Comment(tid, 2, basedir=os.getcwd(),
            dirname="TEST_GROUPID-87654321/").save()
    __path = os.getcwd() + "/static/data/TEST_GROUPID-87654321/" + str(
        tid) + "/"
    __file = str(cid) + ".json"
    assert os.path.exists(__path + __file), "Failed to get last comment!"

    import shutil
    shutil.rmtree(__path)


def testcase_topic_load_full():
    """
    Load topic data (Full)
        - Parse all topic data
        - Any comments and different context
        - Test resource list output
    """
    tid = 123456789098765

    topic_d = "topic-full.json"
    with open("examples/" + topic_d, 'r') as fd:
        td = fd.read()

    from bulk import Topic
    print(Topic(tid, basedir=os.getcwd(), dirname="TEST-5678").talk(
        json.loads(td)))

    __path = os.getcwd() + "/static/data/TEST-5678"
    assert os.path.exists(__path), "Failed to get last comment!"

    import shutil
    shutil.rmtree(__path)


def testcase_group_info():
    """
    Get Group Information by group-id
        - Query group
        - Save data to local.
    """
    gid = 123456789098765

    from conn import Connection
    c = Connection(ident="TESTCASE")

    from bulk import Group
    Group(c, gid, basedir="output").info()  # testing/output

    assert os.path.exists("output/" + str(gid) + "/"), "Failed to get data!"

    os.removedirs("output/")


def testcase_group_topic():
    """
    Get topic list by group-id.
        - Test group object data fills.
        - Make data return in jsonify.
        - Auto paging.
    """
    gid = 123456789098765

    from conn import Connection
    c = Connection(ident="TESTCASE")

    from bulk import Group

    # Fill first
    group_object = Group(c, gid, basedir="output")
    imglink, flink = group_object.save()  # Save data.

    group_object.jsonify()

    from conn import Downloader
    from multiprocessing import Pool, cpu_count
    _pool: multiprocessing.Pool = Pool(cpu_count())
    _pool.starmap(Downloader().acquire, imglink)
    _pool.close()
    _pool.join()
    # Represent all data.
    # group_object.jsonify()  # testing/output
    
    from multiprocessing import Pool, cpu_count
    _pool: multiprocessing.Pool = Pool(cpu_count())
    _st = time.time()
    _pool.starmap(Downloader().acquire, flink)
    _pool.close()
    _pool.join()
    _ed = time.time()
    print("Spend of time: %f " % (_ed - _st))  # Wow! 3MB/s avg. in my test.

    assert os.path.exists(
        "output/static/data/group/" + str(gid) + "/"), "Failed to get data!"


def testcase_filter_file():
    """
    Filter files with options in settings
    """

    gid = 123456789098765

    from utility import value_attachment
    import json

    with open("debug_files.json", 'r') as fd:
        files = json.loads(fd.read())
        x = value_attachment(files["files_task"], basedir="output", gid=gid)

    print(x)

def testcase_timestring():
    """
    Test zTimeStr generation and converting.
        - zTimeStr to datetime object
        - Time to zTimeStr
        - Get current time in zTimeStr
    """
    cur = ztime()
    bl4th3r("Debug", "Current: " + cur)

    assert "%2B08" in cur, "Timezone not output!"

    from datetime import datetime
    bl4th3r("Debug", "Dt->zT: " + ztime(datetime.now()))

    ztd = ztime(cur)

    bl4th3r("Debug", "zT->Dt: " + str(type(ztd)))
    assert isinstance(ztd, datetime), "Convert failed!"

    bl4th3r("debug", "Timestamp: " + ztd.timestamp().__str__())


def testcase_timestring_before():
    """
    Test zTimeStr generate (Before any specific time).
        - Time stamp: "2023-05-10T18:45:55.330+0800"
    """
    from utility import ztime_before
    timestring = "2023-05-10T18:45:55.330+0800"
    # timestring_encoded = "2023-07-29T20%3A25%3A08.641%2B0800"
    ztime_before(timestring)


def testcase_zlink_exceed():
    link_a = "https://images.zsxq.com/AAAAAAAAAAAAAAAAABBBBBBBBBCCCCCCCCCCCDD" \
             "/auto-orient/quality/100!/ignore-error/1&e=1693497599&s=tttteee" \
             "sssstttt&token=abcdabcd-abcdabdcabdacdaccdacdaacdadcacd:A123456" \
             "codecodecodecodecode="
    link_b = "https://images.zsxq.com/lohb_4u4AL-TWwaYi3EjTrU-_-9I?e=16934975" \
             "98&s=testtesttesttes&token=abcdabcd-abcdabdcabdacdaccdacdaacdad" \
             "cacd:A123456codecodecodecodecode="

    from utility import zlink_exceed
    tmval = []

    zlink_exceed(link_a, tmval)
    assert tmval.pop() == 1693497599, "Failed to parse image type-A link."

    zlink_exceed(link_b, tmval)
    assert tmval.pop() == 1693497598, "Failed to parse image type-B link."


def testcase_image():
    """
    Test case for image file download. (1 file, 1 thread, 1 process)
    """
    task = [
        # Paste your image download link here.
    ]
    from conn import Downloader
    Downloader().acquire(task[0], task[1])


def testcase_file():
    """
    Test case for attachment download. (1 file, N thread, C process)
        - C is MIN{CPU cores, COUNT_OF_FILES} <C=1 here>
        - N is your settings `download_thread`
    """
    task = [
        # Paste your file download link here!
    ]

    from conn import Downloader
    Downloader().acquire(task[0], task[1], task[2], task[3], task[4])


def testcase_image_task():
    """
    Test case for attachment download. (3 file, N thread/file, C process)
        - C is MIN{CPU cores, COUNT_OF_FILES}
        - N is your settings `download_thread`
        - Max Memory cost: (file size + 4KB * 3N)* COUNT_OF_FILES
    """
    task = [
        [
           # Paste your image download link here.
        ],
        [
            # Paste your image download link here.
        ],
        [
            # Paste your image download link here.
        ]
    ]

    from conn import Downloader
    from multiprocessing import Pool, cpu_count
    _pool: multiprocessing.Pool = Pool(cpu_count())
    _pool.starmap(Downloader().acquire, task)
    _pool.close()
    _pool.join()


def testcase_file_task():
    """
    Test case for attachment download. (3 file, 8 thread/file, 3 process)
    """
    task = [
        [
            # Paste your file download link here!
        ],
        [
            # Paste your file download link here!
        ],
        [
            # Paste your file download link here!
        ]
    ]

    from conn import Downloader
    from multiprocessing import Pool, cpu_count
    _pool: multiprocessing.Pool = Pool(cpu_count())
    _st = time.time()
    _pool.starmap(Downloader().acquire, task)
    _pool.close()
    _pool.join()
    _ed = time.time()
    print("Spend of time: %f " % (_ed - _st))  # Wow! 3MB/s avg. in my test.


if __name__ == '__main__':
    _case = "standard"  # Default

    # Below is named of testcase, Register here!
    _s_standard = ["modules", "env"]
    _s_connection = ["keys", "header"]
    _s_service = ["account", "group", "users", "timestring",
                  "timestring_before", "zlink_exceed"]
    _s_content = ["comment", "topic_load", "topic_load_comment",
                  "topic_load_full", "group_info", "group_topic"]
    _s_downloader = ["image", "file", "image_task", "file_task"]

    __all = (
            _s_standard + _s_connection + _s_service + _s_content +
            _s_downloader
    )
    __all.sort()  # For every testcase has unique id.
    _s_all = __all
    _single = False

    _target = ""
    # Main procedure of testing.
    if len(sys.argv) >= 2:
        _case = sys.argv[1]
        if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) > 2:
            # Show usage
            if len(sys.argv) == 3:
                if "-s" in sys.argv:
                    _single = True
                    _target = sys.argv[sys.argv.index("-s") + 1]
                else:
                    print("\nErr: Multiple testcase suite select not support.")
            else:
                print('''
Usage: (-h/--help to show this screen)
    %s {SUITE} | -s {one of the testcase name}

Available test suite(s):
                    ''' % sys.argv[0])
                v = list(locals().keys())
                for s in v:
                    if str(s).startswith("_s_"):
                        print(s.replace("_s_", "\t"))
                print("\nAvailable testcase:\n\n  ", end='')
                _idx = 0
                for s in v:
                    if str(s).startswith("testcase_"):
                        _idx += 1
                        print("%-20s" % s.replace("testcase_", ""), end='')
                        print('\t', end='')
                        if _idx % 4 == 0:
                            print("\n  ", end='')
                print("\n\n* Execute `standard` test, without any options.\n")
                exit(-1)
            _case = sys.argv[1]
    else:
        # _case = "__all"
        pass

    if _single and _target:
        try:
            if not _target:
                print("\nErr: No testcase was selected!")
                exit(-1)
            _fn = locals().get("testcase_" + _target)
            _fn()
            exit(0)  # No error
        except TypeError as ex:
            print("\nErr: Testcase `" + _target + "` not found!")
            print(ex)
            exit(-1)  # POSIX - error.
        except Exception as ex:
            if verbose >= 5:
                print(ex)
                exit(-1)  # POSIX - error.

    try:
        __total = len(locals().get("_s_" + _case))
        __idx = 0
        print("Load case: %d, test start within 3s." % __total)
        time.sleep(2)
        for fn in locals().get("_s_" + _case):
            print('\n' + '=' * 20)
            f = locals()["testcase_" + fn]
            print(
                "Case %03d" % (__all.index(fn) + 1) + ': ' + str(
                    f.__doc__).strip() + '\n')
            try:
                f()  # Execute testcase here!
            except Exception as ex:
                print("\n>>! Failed")
                if verbose >= 5:
                    print(ex)
                continue  # Jump to next testcase

            __idx += 1
            print("\n>>> Pass")

        print("\nResult: %d/%d (Passed/Total)." % (__idx, __total))
    except TypeError:
        print("No testcase suite was named: " + _case)
