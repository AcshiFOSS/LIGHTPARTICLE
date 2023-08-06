"""This file belongs to project 'LIGHTPARTICLE', See README for more detail."""

# It's not standalone executable file.

import os
import json
import platform
import random
import threading, queue

import time

from utility import bl4th3r, generate_ua, generate_rid, zlink_exceed
import ctypes

import urllib.error
from error import ENOZSXQ

from settings import debug
from settings import download_instant, download_thread, download_interval
from settings import file_verify


# ### Maintaining(s): _3083 ###
# 2023-07-28    v0.1 Code Review - 1st.
#                   - Add documents (PEP-8 / PEP-257)
#                   - (UI) Improve screen logging line.
#
# 2023-07-29    v0.2 Attachment Downloader
#                   - Add new class Downloader
#
# 2023-07-30    v1.0 Testing and fix Downloader
#                   - Add Range option into header
#                   - Fix off-by-one length mismatch
#                   - Test batch download
#                   - Ensure verify algorithm is correctly
#                   - Only file downloads with download_interval pause.
#
# 2023-07-30    v1.1 Refactor: __header function
#
#


class Connection(object):
    """
    Manage connection to zsxq.com and working with libmweb.

    Attributes:
        cookie:<str>        Cookie on target service.
        ua:<str>            The User-Agent of your browser.
        name:<str>          Connection instance identify.
    Parameters:
        ident:<str>         Identification of connection instance.
    """

    def __init__(self, ident):
        # Load credential with user options.
        try:
            from settings import keyfile
            if len(keyfile) == 0:
                raise ImportError  # Blank Input.
            else:
                with open(keyfile, 'r') as fd:
                    credit = fd.readlines()
                    for c in credit:  # Auto detective cookie and UA string.
                        if c.startswith('#'):
                            continue
                            # Comment with '#' in .key for multiple accounts.
                        if '/' in c:
                            ua = c.replace('\n', '')
                            continue
                        else:
                            if '=' in c:
                                cookie = c.replace('\n', '')
                                continue
        except ImportError:
            keyfile = ""
            bl4th3r("warn", "(CN) No key file! Len: " + str(len(keyfile)))

            try:
                from settings import cookie, ua

                if len(cookie) < 70 and "zsxq_access_token=" not in cookie:
                    raise ImportError  # Necessary cookie string in 71 chars.

                if len(ua) < 32:
                    bl4th3r("warn", "(CN) User-Agent will be generated!")
                    # The shortest UA string length is 32 chars.

            except ImportError:
                bl4th3r("critical", "(CN) No user credential was found!")
                exit(-1)

        # last sanitize user credential
        if ua is None:
            bl4th3r("warn", "(CN) User-Agent will be set to random!")

        if cookie is None:
            bl4th3r("critical", "(CN) Bad key file!")

        self.cookie = cookie
        self.ua = ua

        # Setup connection object naming for trace code.
        self.name = ident[:4] + ident[-4:]  # Split UUID, Pre-4 and Tail-4.

        # Generate User-Agent string if no acceptable UA.
        if self.ua is None and os.path.isfile("useragent.dat"):
            bl4th3r("debug", "Generate a random User-Agent")
            self.ua = generate_ua()
            bl4th3r("info", "Set User-Agent to: " + self.ua[:20])

    @staticmethod
    def __header(*argv) -> dict:
        """
        This function provide HTTP(s) request header options dict generating.

        Parameters:
            argv:<tuple>            The header option values.
        """
        __H = {}

        if len(argv) == 6:

            try:
                from settings import serv
                bl4th3r("INFO", "Target MWeb service: " + serv)
            except ImportError:
                serv = ""
                bl4th3r("warn", "Unknown version of MWeb service!")

            try:
                from settings import libmweb
                if libmweb:
                    header = ctypes.CDLL(
                        os.path.dirname(os.path.abspath(
                            __file__)) + "/libmweb-" + platform.system().lower() + "-" + serv + "/libmweb-x86_64.so"
                    )
                    fn = header.new
                    fn.restype = ctypes.c_char_p
                    fn.argtype = ctypes.c_char_p
                    __H = json.loads(
                        fn(ctypes.c_char_p('$'.join(argv).encode("utf-8"))))
                    return __H
                else:
                    raise FileNotFoundError
            except FileNotFoundError or OSError:  # Disable Clib encryption.
                bl4th3r("critical", "Unknown version of external library...")
        else:
            return __H

    def request(self, url, level, timestamp=0, rid="", sig="",
                step=False, start=0, end=0, fid=0, partial: queue = None):
        """
        Request wrapper with MWeb X verify algorithm. Return HTTP Status.
        :return: (int, JsonObject)
        """

        if rid == "" or not debug:
            __x_requestID = generate_rid()
        else:
            __x_requestID = rid

        if timestamp == 0 or not debug:
            __x_timestamp = str(time.time().__ceil__())  # Round up
        else:
            __x_timestamp = str(timestamp)

        _status = 0
        _cookie = False
        _isFile = False
        _isImage = False

        bl4th3r("INFO", "Set RID: " + __x_requestID)
        bl4th3r("INFO", "UA: " + self.ua[:30] + " ...")

        # v1.1 Move __H outside switch-case statements.
        _refer = "https://wx.zsxq.com"
        __H = self.__header(str(level).upper(), url, __x_timestamp,
                            __x_requestID, _refer, self.ua)

        match str(level).upper():
            case "XSEC":
                _cookie = True
            case "USER":
                _cookie = True
                _isFile = True
                # Add range request header option.
                __H["Range"] = "bytes=%d-%d" % (start, end)
                bl4th3r("debug", "Current slice -> Range=" + __H["Range"])
                bl4th3r("debug", "%CN% " + str(__H))
            case "BROWSER":
                _isImage = True
            case _:  # No Extra header options
                __H = {}

        if step:
            bl4th3r("debug", "%XS% Ensure request signature is excepted!")

        if debug and step:
            __flag = False  # Keep testcase offline.
            if sig != "" and _isFile is not True:  # Need Check signature.
                bl4th3r("debug", "Check signature ...")
                if __H["X-Signature"] == sig:
                    bl4th3r("info", "OK - Signature test passed!")
                    __flag = True
                else:
                    bl4th3r("error", "Failed - Signature not acceptable!")
                    bl4th3r("critical", "Current in " + __H["X-Signature"])
                    exit(-1)

            if not __flag:  # Step mode.
                if input("\nSend this request? [Y/N]: ").lower() == "y":
                    pass
                else:
                    return ()
            else:  # Signature test pass. Skip for sending this.
                return ()

        __link = url.split('/', maxsplit=3)[3]

        if len(__link) > 45:
            bl4th3r("DEBUG", "Location: /" + __link[:40] + "...")
        else:
            bl4th3r("DEBUG", "Location: /" + __link)

        bl4th3r("DEBUG", "Current Cookie: " + self.cookie[:20] + " ...")

        if _cookie:
            __H['Cookie'] = self.cookie

        bl4th3r("DEBUG", "Current Headers: " + str(__H)[:20] + " ...")

        # Do request.
        from urllib.request import Request, urlopen
        try:
            resp = urlopen(Request(url, headers=__H))

            if _isImage:
                return resp.status, resp.read()  # Return Blob data.
            elif _isFile:
                if isinstance(partial, queue.Queue):
                    partial.put(resp.read())
                    bl4th3r("debug", "%CN% Partial data put into queue.")
                else:
                    bl4th3r("critical", "%CM% Data must be push back into Q!")
            else:
                _status = resp.status
                resp = json.loads(resp.read())
                # Check response HTTP_STATUS / 200
                if debug:
                    bl4th3r("INFO", "%CNR% Resp-Status: " + str(_status))
                    bl4th3r("DEBUG",
                            "%CNR% Resp-Content: " + str(resp)[:20] + "...")
                # Translate code to error message

                bl4th3r("INFO",
                        "(CN) Request Succeeded: " + str(resp["succeeded"]))

                if str(resp["succeeded"]).endswith("se"):  # false
                    eno = resp["code"]
                    bl4th3r("critical", "Reason: " + ENOZSXQ(eno))

                return _status, resp["resp_data"]

        except urllib.error.HTTPError as e:  # caught it first.
            bl4th3r("debug", "%CN% HTTP status: " + str(e.code))
            if e.code.__str__().startswith("4"):
                bl4th3r("warn", "%CN% File link need refresh! ID: " + str(fid))
                return e.code, None
            # ... this branch of codes is not in use. Multi-threading
            # downloader will cause too many HTTP-4xx errors. That's AWFUL!
            # TODO: Add an offline url parameter `e`(exceed-time-limit) check!
            # -Fix: Use API._time_exceed(__link) to check the links before
            #       request.
        except urllib.error.URLError:
            bl4th3r("critical", "(CN) Internet connection down!")


class Downloader(object):
    """
    General file downloader.

    Attributes:
        output:<str>        Path of output
        basedir:<str>       Export directory
        _threads:<list>     List of download task (Thread)
    """

    def __init__(self, basedir=None, output="/static/data/uploads/"):
        self.basedir = basedir if basedir else os.getcwd()
        self.output = output
        self._threads = []
        self._furl = None
        self._q = None

    def acquire(self, url, name, fid=None, length=None, checksum=None) -> int:
        """
        Provide multi-threading download function. Return the data length that
        was downloaded. This function will work with multiprocessing in main
        thread for improving speed.

        Parameters:
            url:<str>       Download task description dict
            name:<str>      Output filename
            fid:<int>       File unique
            length:<int>    File length
            checksum:<str>  File hash checksum
        :task:
            For images {link, filename}
            For files {link, filename, length, hash}
        """
        b = 0
        types = url.split('/')[2].split('.')[0]
        level = "user" if types == "files" else "browser"
        self._furl = url

        __path = self.basedir + self.output + str(types) + '/'
        if not os.path.exists(__path):
            os.makedirs(__path)
        # Check exceed time limit
        from api import API
        print(name)
        if not zlink_exceed(self._furl):
            if types == "files":  # Refresh
                try:
                    _, resp = Connection("FEED-BEEF").request(
                        url=API.file_link(fid), level='xsec'
                    )
                    url = resp["download_url"]
                    if '/' not in url:
                        raise KeyError  # resp["download_link"] not found!
                except KeyError:
                    bl4th3r("error", "Failed to refresh: " + str(fid))
            if types == "images":  # Notify and redo all works!
                bl4th3r("critical",
                        "(D) Image link unavailable. Need reinitialization!")
        match types:
            case "images":
                if not download_instant:  # Get image ASAP if instant download.
                    time.sleep(
                        random.randint(0, download_interval)
                    )  # Junk pause X seconds.
                _, data = Connection("FEED-CAFE").request(url, level)
                # storage

                if data:
                    try:
                        with open(__path + name, 'wb') as fd:
                            b = fd.write(data)
                    except IOError:
                        bl4th3r("error", "(D) Missing privileges!")
                else:
                    bl4th3r("error", "(D) Empty data")
                return b
            case "files":
                if not download_instant:  # Get image ASAP if instant download.
                    time.sleep(
                        random.randint(0, download_interval)
                    )  # Junk pause X seconds.
                self._q = queue.Queue()
                # multi-threading download in manually.
                __slice = int(length) // download_thread
                # __chunk_start = range(0, length, __slice)
                # TODO: Fixup Off-by-One err. (abandon `__floor__`)
                # -Fix: round up __slice

                # Add threading task
                for i in range(download_thread):
                    start = __slice * i
                    end = start + __slice - 1

                    if i + 1 == download_thread:
                        end = length  # Last piece, download all leavings.

                    self._threads.append(
                        threading.Thread(
                            target=Connection("FEED-BEEF").request,
                            kwargs={
                                "url": url,
                                "level": level,
                                "start": start,
                                "end": end,
                                "fid": fid,
                                "partial": self._q
                            }
                        )
                    )
                    if end == length:
                        break  # Jump out if download task cover all ranges.
                for t in self._threads:
                    t.start()
                    t.join()

                __pre_file = b""
                while not self._q.empty():
                    idx = 0
                    __pre_file += self._q.get()
                    with open("temp-" + str(idx), 'wb') as fd:
                        fd.write(__pre_file)

                __chk_pass = True
                if file_verify:  # Multi-download, single write.
                    if len(__pre_file) == length:
                        from hashlib import sha256
                        _c = sha256(__pre_file).hexdigest()
                        bl4th3r("debug", "(D) Download: " + _c)
                        if _c != checksum:
                            __chk_pass = False
                            bl4th3r("warn", "(D) Wrong checksum: " + checksum)
                        else:
                            bl4th3r("info", "(D) Download done, verified!")
                    else:
                        __chk_pass = False
                        bl4th3r("warn", "(D) length of download is mismatch!")
                        bl4th3r("debug", "%D% except: " + str(length))
                        bl4th3r("debug", "%D% Rx Len: " + str(len(__pre_file)))
                if not file_verify or (file_verify and __chk_pass):
                    with open(__path + name, 'wb') as fd:
                        fd.write(__pre_file)
            case _:
                return -1
