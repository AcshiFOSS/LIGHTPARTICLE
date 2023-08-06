# This file belongs to project 'LIGHTPARTICLE', See README for more details.

"""
Provide all data structure and parser. Some function will request remote
resource instantly. Fetch data and storage JSON files to local disk in our
pre-specified directory structure. All datasets will be rendered by frontend.

* This is not a standalone executable module.
"""

import os
import json

import conn
from api import API
from utility import bl4th3r, ztime_before

from error import ENOZSXQ
from urllib.error import *
from conn import Connection

from settings import debug
from settings import topic_max, comment_max, download_instant, get_download_url
from settings import download_instant_image_only

from abc import abstractmethod


# ### Maintainer(s): _3083 ###
# 2023-07-23    Bump v0.1(init), It's works.
#
# 2023-07-28    Code Review - 1st.
#                 - <Func> Keep output path is excepted.
#                   - Fix all `output` to `basedir`
#                   - Fix unexpected /static/data/ create.
#                 - <Code> Fix Typo.
#                 - <UI> Optimized all debug output.
#                   - Fix logging filtration by level.
#                 - <DOC> Complete any necessary API docstring.
#                 - <Sec> Ensure attributes defining.
#
# 2023-07-30    v1.0 - Fix
#               Ensure all resource object in type of list.
#                 - For map() to Downloader.acquire()
#                 - Add download immediately support
#                 - Short useless codes.
#                   - Tag with <Files in comment - E001>
#                      Memo for file info parsing if comment with attachment.
#                   - Tag with <Files in question - E003>
#                      - Memo for file info parsing if question with attachment.
#                 - Fix Topic(dirname) as necessary parameters.
#

class Blob(object):
    """
    Basic class of all data instance.

    Attributes:
        id:<int>        Resource unique identifier.
        _output:<str>   Current work directory or specified.
        _basedir:<str>     Prefix of the export path.
        _dir:<str>      Export directory.

    Parameters:
        oid:<int>       Object ID.
        basedir:<str>   Data export base directory name.
    """

    def __init__(self, oid, basedir=None, dirname=None):
        """
        Initialize export path with customized basedir.
        If access any data class with member function.
        """

        self.id = oid

        self._basedir = basedir if basedir else os.getcwd()
        self._dir = "/static/data/"

        self._basedir = basedir if basedir else self._basedir
        # self._dir += (dirname + '/') if dirname else "/"  # Append

        if dirname:
            dirname += "/"
            self._dir += dirname
        else:
            pass

        bl4th3r("debug", "%F% _Dir path: " + self._dir)

        self._output = self._basedir + self._dir

        bl4th3r("debug", "%F% Full object path: " + self._output)

        if not os.path.exists(self._output):
            bl4th3r("debug", "%F% Create directory!")
            os.makedirs(self._output)

    # For giving a testing entry, `save` and `fetch` was being detached.

    @abstractmethod
    def _acquire(self):
        """Interface of data download, Must implement / Override in the next."""
        bl4th3r("debug", "%B% Missing the necessity function of data acquire!")
        raise NotImplementedError

    @abstractmethod
    def save(self):
        """Save data on local disk."""
        bl4th3r("debug", "%B% Missing necessity function of data storage!")
        raise NotImplementedError


class User(Blob):
    """
    Abstract user information which was combined with topics or comments. This
    class also be used to describe your self account.

    The file path ${CWD}/static/data/user/ by default.

    Attributes:
        name:<str>     The (nick)name.
        avatar:<str>   Avatar download link.
        location:<str> The network location.

    Parameters:
        uid:<int>       User unique ident. (None as your self account.)
        name:<str>      User nickname.
        avatar:<str>    Avatar download link.
        location:<str>  The network location.

    * All parameters can be used to create User instance manually.
    """

    def __init__(self, uid=None, name=None, avatar=None, location=None,
                 basedir=None, dirname="users"):
        # Keys, # `uid` can be set to None.(your self account)
        super().__init__(uid, basedir=basedir, dirname=dirname)
        self.name = name
        self.avatar = avatar
        self.location = location

        # Configure file of <User_ID>.json location:

        self._filename = None

    def _acquire(self) -> bool:
        """
        (Protected) Download details of user by UID. Return succeeded counts.
        """
        # Check path is existed or not. (Create if that was not exist.)

        __link = API.user() if self.id is None else API.user(uid=self.id)
        self._filename = str(self.id) + ".json" if self.id else "self.json"

        if os.path.exists(self._output + self._filename):
            bl4th3r("warn", "(U) Ignore duplicate: " + str(self.id))
            return False

        # Fetch a new user details.
        __resp: dict = {}

        try:
            c = Connection("face-beef")  # DEBUG INDI.: 0xFACE-BEEF
            __resp = c.request(__link, "xsec")[1]["user"]
        except HTTPError as ex:
            bl4th3r("critical", "(U) Server Reason: " + ENOZSXQ(ex.code))
            bl4th3r("debug", "%U% HTTP failed: " + ex.reason)
        except KeyError:
            bl4th3r("error", "(U) Unreachable user: " + str(self.id))

        if len(__resp) <= 5:
            _, _, self.name, self.avatar, self.location = __resp.values()

            if debug:
                bl4th3r("info", "(U) New user was added: ")
                print(json.dumps(
                    {
                        k: v for k, v in vars(self).items()
                        if not k.startswith('_')
                    }, indent=2, ensure_ascii=False)
                )
        else:
            bl4th3r("debug", "%U% Server change the frame of USER!")
            if debug:
                print(json.dumps(__resp, indent=2))
            return False

        return True

    def save(self) -> tuple:
        """
        Save current class User instance to disk as a json file named with UID.
        Return a tuple which contain user describe dict.
        """

        # Check path, then _acquire when output path is empty.
        bl4th3r("debug", "%F% Save the user data to disk.")
        if not self._acquire():
            return ({},)

        # Store
        udata = {k: v for k, v in vars(self).items() if not k.startswith('_')}

        try:
            with open(self._output + self._filename, 'w') as fd:
                fd.write(json.dumps(udata))
        except IOError:
            bl4th3r("error", "(U) Failed to write files!")
            return ()

        return (udata,)

    def __call__(self, *args, **kwargs):  # Alias for shortest our code.
        self.save()


class Comment(Blob):
    """
    Comment under every publish post. Support to parse reply message and user
    mentioned others.

    The file path ${CWD}/static/data/comment/{Topic_ID}/ by default.
    If you want to keep comment under topic path, you need change the `dirname`.

    Attributes:
        topic_id:<int>          Which topic that the comment belongings.
        comment_total:<int>     Counts of comment.
        images:<list>           The image attachments of comment.
        comment:<list>          All comment records. (For return)

    Parameters:
        tid:<int>               Topic unique id.
        count:<int>             Counts of comment which under the topic.
        basedir:<str>            Comment data file export path.

    """

    def __init__(self, tid, count, dirname="comment", basedir=None):
        dirname = dirname if dirname else "comment"  # For Topic.talk/question()
        # If you need dirname /static/data/ append /groups/{GID} tailer.
        super().__init__(tid, basedir=basedir, dirname=dirname + "/" + str(tid))
        self.topic_id = self.id  # A comment must below at a topic.
        self.comment_total = count

        # For one comment
        self.images = []
        self._image_resource = []

        # For process indicator
        self._cursor = 0
        self._last_comment = None

        # Configs
        self._output += "/"  # Comment save in topic-id named directory.

        # For all comments under a topic.
        self.comment = []  # Record all comment id for return to Topic object.

        # 1. The __init__() can not return anything.
        # 2. Comments of topic will be increased as time goes on.
        # -- So class Comment without any de-duplication function.

    # Comment with some dependency values (Topic-ID), so `fetch` is `saved`.
    # Combine in one function is a clear way to parse nested comment.
    def _acquire(self, end_time=None, is_reply=False, reply=None) -> tuple:
        """
        (Protected) Get comment data to local JSON files.

        Parameters:
            end_time:<str>      For paging. The end_time need before last one.
            is_reply:<bool>     Flag the type of reply message.
            reply:<list>        Data object of reply comments.
        """
        _no_more = False

        if not is_reply:
            bl4th3r("debug", "%CM% Timestamp: " + str(end_time))

            _link = API.comment(self.topic_id, end_time=end_time)

            try:
                c = conn.Connection("face-cafe")  # DEBUG INDI.: FACE-CAFE
                try:
                    r = c.request(_link, "xsec")[1]["comments"]
                except KeyError:
                    r = []  # No comments in fact!!! even comment_counts=1

                _no_more = False if len(r) else True  # Check next page...
            except HTTPError as ex:
                bl4th3r("critical", "(CM) Server Reason: " + ENOZSXQ(ex.code))
                bl4th3r("debug", "%CM% HTTP failed: " + ex.reason)
                return ()  # No more tries? - Any error will record on server.
        else:
            r = reply  # Override context for parsing reply message. Fake fork.

        for _cmt in r:  # TODO: Optimize | But element of JSON is not stability.
            cid = _cmt["comment_id"]
            ctime = _cmt["create_time"]
            owner = _cmt["owner"]["user_id"]
            text = _cmt["text"]

            bl4th3r("debug", "%CM% Handle comment: " + str(cid))
            bl4th3r("debug", "%CM% IsReply: " + str(is_reply))

            self._last_comment = ctime
            self._cursor += 1

            User(owner, basedir=self._basedir).save()

            # Handle replies in comment.
            try:
                reply_count = _cmt["replies_count"]
                reply = _cmt["replied_comments"]
                _count = len(reply)
                if reply_count != _count:
                    bl4th3r("warn", "(CM) Some replies were hiding.")
                # self._cursor += reply_count
                # _acquire caller is instance of class Comment.
                self._acquire(is_reply=True, reply=_cmt["replied_comments"])
            except KeyError:
                pass  # No reply comment

            reply_to = 0
            if is_reply:
                try:
                    reply_to = _cmt["repliee"]["user_id"]  # *Ignore this typo*
                    User(reply_to, basedir=self._basedir).save()
                except KeyError:
                    pass  # IT's just replied a comment of others mention.

            # Images
            try:
                _images = _cmt["images"]

                for _cmt_img in _images:
                    _img_id = _cmt_img["image_id"]
                    _img_type = _cmt_img["type"]

                    # TODO: Optimize | Step-down picture quality.
                    _img_link = "#"
                    try:
                        _img_link = _cmt_img["original"]["url"]
                    except KeyError:
                        try:
                            _img_link = _cmt_img["large"]["url"]
                            if debug:
                                bl4th3r("debug", "%CM% Image downgrade-> large")
                        except KeyError:  # thumbnail
                            try:
                                _img_link = _cmt_img["thumbnail"]["url"]
                                if debug:
                                    bl4th3r("debug", "%CM% Only thumbnail.")
                            except KeyError:
                                bl4th3r("error", "(CM) No resource link!")
                                bl4th3r("debug",
                                        "%CM% Server change the frame: IMAGE!")

                    self._image_resource.append(
                        [_img_link, str(_img_id) + '.' + str(_img_type)]
                    )
                    # Fix: Support download images instantly!
                    # TODO: Add here a downloader with settings filter.
                    if download_instant:
                        from conn import Downloader
                        Downloader(basedir=self._basedir).acquire(
                            url=_img_link,
                            name=str(_img_id) + '.' + str(_img_type)
                        )
                    d = {"id": _img_id, "type": _img_type, "origin": _img_link}
                    # Only a month period to download images.
                    # TODO: Refresh download link in downloader with object id.

                    if debug:
                        bl4th3r("debug", "%CM% New image: ")
                        print(json.dumps(d, indent=2, ensure_ascii=False))

                    self.images.append(d)

            except KeyError:
                pass  # No images

            # <Files in comment - E001>
            # Not In Use (<=2.39.0), Attachment with comment not support in
            # the MWeb v2.40. Refer to the class `Topic` for this section.

            d = {
                "comment_id": cid,
                "create_time": ctime,
                "text": text,
                "images": self.images,  # if it has
                # "files": self.files,  # if it has
                "owner": owner,
                "reply_to": reply_to
            }

            # save
            # /static/data/{DIRNAME | comment}/TID/CID.json
            if debug:
                bl4th3r("Debug", "%F% Writes: " + str(cid) + " comments.")

            try:
                with open(self._output + str(cid) + ".json", 'w') as fd:
                    fd.write(json.dumps(d, indent=2, ensure_ascii=False))
            except IOError:
                bl4th3r("critical", "(CM) No permission(s) to save file!")

            if debug:
                if is_reply:
                    bl4th3r("debug", "%CM% Split Comment: ")
                else:
                    bl4th3r("debug", "%CM% Comment: ")
                print(json.dumps(d, indent=2, ensure_ascii=False))

            self.comment.append(d)

        # if self.current_comment_idx != self.comment_total:
        if self.comment_total > comment_max and not _no_more:
            bl4th3r("Info", "(CM) New time range start...")
            self._acquire(end_time=ztime_before(self._last_comment))
            # Pray for get all...
        # <Files in comment - E001>
        # return (self.comment, self._image_resource, self._file_resource)
        return self.comment, self._image_resource, []

    def save(self) -> tuple:
        """
        Alias to Comment._acquire(). without time range filter for initialize
        data downloading.
        """
        return self._acquire()

    def __call__(self, *args, **kwargs) -> tuple:
        return self.save()


class Topic(Blob):
    """
    To gathering a topic details. Include save data to local disk. This is a
    major structure in this project.

    Attributes:
        id:<int>        Topic unique indent.

    Parameters:
        tid:<int>       (same as `id`)
        basedir:<str>    The path of data export.

    """

    # Assuming all handler return a same structure. To present in 3-W formal.
    # Who       What                        When
    # OwnerID   text/comment and files      zTimeStr

    # Caution: All comments data in topic is dynamically update. All topics
    # fetch under `force update` by default. Even the topic JSON file already
    # in output directory.

    def __init__(self, tid, dirname, basedir=None):

        if not dirname:
            bl4th3r("warn", "(T) You may got a confusion export path.")

        super().__init__(tid, basedir=basedir, dirname=dirname)

        # Configs
        self._file = str(tid) + ".json"
        self._dirname = dirname
        # base + /static/data/{dirname}/{topic_id}
        #                     ^groups/{GID}
        self._output += "/"
        # Just a JSON file, make directory when topic has comment.
        #
        # if not os.path.exists(self._output):
        #     os.makedirs(self._output)

    def question(self, topic, with_file=False) -> tuple:
        """
        Parse data in "Q&A" content type.

        Parameters:
            topic:<object>      Topic context.
            with_file:<bool>    Download file or not.
        """
        _type = "question"

        _id = topic["topic_id"]
        owner = topic["question"]["owner"]["user_id"]

        User(uid=owner, basedir=self._basedir).save()  # Storage user info.
        # The Quest User, Answer is owner.

        _question = topic["question"]["text"]
        _question_images = []

        _answer = topic["answer"]["text"]
        _answer_images = []

        comments = []  # If it has

        images_link = []  # If it has
        files_link = []

        _question_files = []  # If it has
        _answer_files = []

        comment_count = topic["comments_count"]
        create_time = topic["create_time"]

        _idx = 0
        if comment_count > 0:  # Get comments, save in topic named sub-folder.
            cdata = Comment(tid=_id, count=comment_count,
                            basedir=self._basedir, dirname=self._dirname).save()

            comments = cdata[0]
            if cdata[1]:
                images_link.append(cdata[1])

            if cdata[2]:
                files_link.append(cdata[2])

        for kw in ["question", "answer"]:
            # Images (Question and Answer)
            try:
                _q_images = topic[kw]["images"]

                for _object_img in _q_images:
                    _img_id = _object_img["image_id"]
                    try:
                        _img_link = _object_img["original"]["url"]
                    except KeyError:
                        _img_link = _object_img["large"]["url"]
                    # Step-down picture quality.

                    _img_type = _object_img["type"]

                    # New connection to download it! (Need batch mode support??)
                    # TODO - Add image links to download list.
                    # -Fix: Added.
                    images_link.append(
                        [_img_link, str(_img_id) + "." + _img_type]
                    )

                    if download_instant:
                        from conn import Downloader
                        Downloader(basedir=self._basedir).acquire(
                            url=_img_link,
                            name=str(_img_id) + '.' + str(_img_type)
                        )

                    if kw == "question":
                        _question_images.append({
                            "id": _img_id,
                            "type": _img_type,
                            "origin": _img_link  # Only ! month available.
                        })

                    else:
                        _answer_images.append({
                            "id": _img_id,
                            "type": _img_type,
                            "origin": _img_link  # Only ! month available.
                        })
            except KeyError:
                pass  # No images found

            try:
                # Files  - Q&A without files. version <= 2.39.0
                _q_files = topic[kw]["files"]

                _file_link = "#"
                _file_name = ""
                _file_size = 0
                _file_hash = ""
                _file_ctime = ""
                _file_down = 0
                _file_topic = _id

                for _f in _q_files:
                    _file_id = _f["file_id"],

                    if with_file:
                        _file_link = Connection("cafe-beef").request(
                            API.file_link(_file_id), "xsec")[1]["download_url"]
                        # Static ident: cafe-beef

                    _file_name = _f["name"],
                    _file_hash = _f["hash"],
                    _file_ctime = _f["create_time"]
                    _file_size = _f["size"]
                    _file_down = _f["download_count"]

                    files_link.append(
                        [_file_link, _file_name[0], _file_id[0], _file_size,
                         _file_hash[0], _file_down, _file_topic]
                    )

                    if download_instant and not download_instant_image_only:
                        from conn import Downloader
                        Downloader(basedir=self._basedir).acquire(
                            url=_file_link,
                            name=_file_name,
                            fid=_file_id,
                            length=_file_size,
                            checksum=_file_hash,
                        )

                    if kw == "question":
                        _question_files.append(
                            {
                                "id": _file_id,
                                "name": _file_name,
                                "origin": _file_link,
                                "hash": _file_hash,
                                "size": _file_size,
                                "create_time": _file_ctime,
                            }
                        )
                    else:
                        _answer_files.append(
                            {
                                "id": _file_id,
                                "name": _file_name,
                                "origin": _file_link,
                                "hash": _file_hash,
                                "size": _file_size,
                                "create_time": _file_ctime,
                            }
                        )
            except KeyError:
                pass  # No files found.

        d = {
            "topic_id": _id,
            "type": _type,
            "owner": owner,
            "question": _question,
            "answer": _answer,
            "comment": comments,  # []
            "question_images": _question_images,  # []
            "answer_images": _answer_images,  # []
            "question_files": _question_files,  # []
            "answer_files": _answer_files,  # []
            "create_time": create_time,
        }
        # /static/data/group/12345678/1234567890.json
        with open(self._output + self._file, 'w') as fd:
            fd.write(json.dumps(d))

        if debug:
            bl4th3r("debug", "Data Rx: ")
            print(json.dumps(d, indent=2, ensure_ascii=False))

        return d, images_link, files_link

    def talk(self, topic, with_file=False) -> tuple:
        # /static/data/group/12345678/
        _type = "talk"

        _id = topic["topic_id"]
        bl4th3r("info", "(T) Topic <talk> id: " + str(_id))
        owner = topic["talk"]["owner"]["user_id"]

        User(uid=owner, basedir=self._basedir).save()  # Storage user info.
        # The Quest User, Answer is owner.

        try:
            text = topic["talk"]["text"]
        except KeyError:
            text = ""  # Talk text can be empty (image only)

        images = []
        files = []

        images_link = []  # If it has
        files_link = []

        comments = []  # If it has

        comment_count = topic["comments_count"]
        create_time = topic["create_time"]

        if comment_count > 0:  # Get comments, save in topic named sub-folder.
            cdata = Comment(tid=_id, count=comment_count,
                            basedir=self._basedir, dirname=self._dirname).save()

            comments = cdata[0]
            if cdata[1]:
                images_link.append(cdata[1])
            if cdata[2]:
                files_link.append(cdata[2])

        try:
            _q_images = topic["talk"]["images"]
            if debug:
                bl4th3r("debug", "%T% Topic with images!")

            for _object_img in _q_images:
                _img_id = _object_img["image_id"]

                _img_link = "#"
                try:
                    _img_link = _object_img["original"]["url"]
                except KeyError:
                    try:
                        if debug:
                            bl4th3r("warn", "(T) Downgrade image level->large")
                        _img_link = _object_img["large"]["url"]
                    except KeyError:  # thumbnail
                        try:
                            if debug:
                                bl4th3r("warn",
                                        "(T) Downgrade image level->thumb.")
                            _img_link = _object_img["thumbnail"]["url"]
                        except KeyError:
                            bl4th3r("error", "(T) No resource link here!")

                # Step-down picture quality.

                _img_type = _object_img["type"]
                bl4th3r("debug", "%T% new image type: " + str(_img_type))

                # New connection to download it! (Need batch mode support??)
                # TODO - Async add image links to download list.
                if download_instant:
                    from conn import Downloader
                    Downloader(basedir=self._basedir).acquire(
                        url=_img_link,
                        name=str(_img_id) + '.' + str(_img_type)
                    )

                images_link.append(
                    [_img_link, str(_img_id) + "." + _img_type]
                )
                image_attr = {
                    "id": _img_id,
                    "type": _img_type,
                    "origin": _img_link  # Only ! month available.
                }
                images.append(image_attr)

        except KeyError:
            pass  # No images

        try:
            _q_files = topic["talk"]["files"]

            for _f in _q_files:
                _file_id = _f["file_id"]

                _file_link = "#"
                _file_name = ""
                _file_size = 0
                _file_hash = ""
                _file_ctime = ""
                _file_topic = _id

                _file_id = _f["file_id"],

                if with_file:
                    _file_link = Connection("cafe-beef").request(
                        API.file_link(_file_id), "xsec")[1]["download_url"]
                    # Static ident: cafe-beef

                _file_name = _f["name"],
                _file_hash = _f["hash"],
                _file_ctime = _f["create_time"]
                _file_size = _f["size"]
                _file_down = _f["download_count"]

                files_link.append(
                    [_file_link, _file_name[0], _file_id[0], _file_size,
                     _file_hash[0], _file_down, _file_topic]
                )

                # Static ident: cafe-beef
                bl4th3r("debug", "%T% Catch file: " + str(_file_id))

                #
                # _file_link = Connection("cafe-beef").request(
                #     API.file_link(_file_id), "xsec")[1]["download_url"]
                # _file_name = _f["name"],
                # _file_hash = _f["hash"],
                # _file_ctime = _f["create_time"]
                # _file_size = _f["size"]
                #
                # files_link.append(
                #     [_file_link, _file_name, _file_id, _file_size, _file_hash]
                # )

                if download_instant and not download_instant_image_only:
                    from conn import Downloader
                    Downloader(basedir=self._basedir).acquire(
                        url=_file_link,
                        name=_file_name,
                        fid=_file_id,
                        length=_file_size,
                        checksum=_file_hash,
                    )

                files.append(
                    {
                        "id": _file_id,
                        "name": _file_name,
                        "origin": _file_link,
                        "hash": _file_hash,
                        "create_time": _file_ctime,
                        "size": _file_size
                    }
                )
        except KeyError:
            pass  # No files found.

        d = {
            "type": _type,
            "topic_id": _id,
            "owner": owner,
            "text": text,
            "comment": comments,  # []
            "files": files,  # []
            "images": images,  # []
            "create_time": create_time
        }

        # /static/data/group/12345678/1234567890.json
        with open(self._output + self._file, 'w') as fd:
            fd.write(json.dumps(d))

        if debug:
            bl4th3r("Debug", "(T) Topic: ")
            print(json.dumps(d, indent=2, ensure_ascii=False))

        return d, images_link, files_link

    def _acquire(self) -> dict:

        # Static ident: beef-cafe
        c = conn.Connection("beef-cafe").request(
            API.topic_info(self.id), "xsec"
        )

        return json.loads(c["topic_info"])

    def save(self):
        return self._acquire()


# Group Object, Not a Blob, but it can be a blob inherit.
class Group(Blob):
    """
    Group/Channel description.

    Attributes:
        conn:<Connection>           Connection handler instance.
        name:<str>                  Group name.
        description:<str>           Group description.
        owner_id:<int>              Group owner user id.
        topic_total:<signed int>    Counts of topics.
        file_total:<signed int>     Counts of files.
        topic_digest:<signed int>   Counts of digest talk.
        topic_answer:<signed int>   Counts of Q&A talk.
        topics:<list>               Topic list.
        comments:<list>             Comment list.
        files:<list>                Files list.
        files_link:<list>           Files download link list.
        images:<list>               Image list.
        images_link:<list>          Image download link list.
        _cur_idx:<int>              The count of parsed talk content.
        last_update:<str>           Last update date<zTimeString>.
        create_time:<str>           Group create timestamp<zTimeString>.
        update_time:<str>           Content update timestamp<zTimeString>.

    Parameters:
        c:<object>                  Connection context.
        gid:<int>                   Group ID.
        basedir:<str>               Output directory.
        dirname:<str>               Export path.
    """

    # Override
    def __init__(self, c: Connection, gid, basedir=None, dirname=None):
        self._dirname = dirname if dirname else "group/" + str(gid)
        super().__init__(gid, basedir=basedir, dirname=self._dirname)

        self.conn = c

        self.name = None
        self.description = None
        self.owner_id = None

        self.topic_total = -1
        self.file_total = -1
        self.topic_digest = -1
        self.topic_answer = -1

        self.topics = []
        self.comments = []

        self.files = []
        self.files_link = []
        self.images = []
        self.images_link = []

        self._cur_idx = 0
        self.last_update = None

        self.create_time = None
        self.update_time = None

        self._fdown = get_download_url

    def info(self):
        if not os.path.exists(self._output):
            bl4th3r("debug", "%G% New Group: " + str(self.id))
            os.makedirs(self._output)

        bl4th3r("debug", "%F% Group.Info output: " + self._output)

        _link = API.group_info(self.id)

        try:
            resp = self.conn.request(_link, "xsec")[1]["group"]
        except HTTPError as ex:
            bl4th3r("warn", "HTTP error: " + ex.reason)
            _status = ex.code
            bl4th3r("warn", "Server Reason: " + ENOZSXQ(_status))
            return ()  # No more retries? - Any error will record on server.

        if self.id == resp["group_id"]:
            self.name = resp["name"]
            self.description = resp["description"]
            self.owner_id = resp["owner"]["user_id"]
            self.create_time = resp["create_time"]
            self.update_time = resp["update_time"]
            self.topic_total = resp["statistics"]["topics"]["topics_count"]
            self.topic_answer = resp["statistics"]["topics"]["answers_count"]
            self.topic_digest = resp["statistics"]["topics"]["digests_count"]
            try:
                self.file_total = resp["statistics"]["files"]["count"]
            except KeyError:
                self.file_total = 0  # No files

            User(uid=self.owner_id, basedir=self._basedir).save()

        _d = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner_id,
            "topic_count": self.topic_total,
            "topic_count_answer": self.topic_answer,
            "topic_count_digest": self.topic_digest,
            "file_count": self.file_total,
            "create_time": self.create_time,
            "update_time": self.update_time
        }

        if debug:
            print(json.dumps(_d, indent=2, ensure_ascii=False))

        # Hibernate
        with open(self._output + "/" + "info.json", 'w') as fd:
            fd.write(json.dumps(_d))

    def topic(self, end_time=None, scope="all", begin_time=None) -> int:
        """
        Query any topic id in the group.
        - ALl topic list. (by dfl.)
        - One topic your specify by tid. (tid=1234567890987654)
        - Filters:
            - Only digest topics.  (digest=True)
            - Filter topic by end_time.  (end_time=TIMESTRING)
        """
        # Check info was got.
        if self.topic_total < 0:
            bl4th3r("debug", "%G% Unknown counts of topic. ")
            self.info()
            bl4th3r("debug", "%G% Current _output: " + self._output)

        bl4th3r("Info", "(G) Timerange before: " + str(end_time))
        bl4th3r("debug", "%G% Fetch " + str(topic_max) + " topic/req.")

        _link = API.topic_list(self.id, count=topic_max, scope=scope,
                               end_time=end_time, begin_time=begin_time)

        __resp = any({})
        # Request data - Get all topic list and update last time stamp.
        try:
            __resp = self.conn.request(_link, "xsec")
        except HTTPError as ex:
            bl4th3r("warn", "(G) HTTP error: " + ex.reason)
            _status = ex.code
            bl4th3r("warn", "(G) Server Reason: " + ENOZSXQ(_status))

        # Check valid.
        if __resp[0] != 200:  # Connection Failed!
            bl4th3r("critical", "(G) Connection failure. retry!")

        if len(__resp[1]) == 0:
            bl4th3r("critical", "(G) Receive empty data.")

        # Merge data to be storage.
        __resp = __resp[1]["topics"]  # "topics:{}

        __no_more = False
        if len(__resp) == 0:
            __no_more = True

        for t in __resp:
            self.last_update = t["create_time"]
            _tid = t["topic_id"]
            bl4th3r("Debug", "(G) Publish content type: " + str(t["type"]))
            match t["type"]:  # First letter in q&a or talk
                case "q&a":
                    _st = Topic(tid=_tid,
                                basedir=self._basedir,
                                dirname=self._dirname
                                ).question(t, with_file=self._fdown)
                    # /static/data/group/12345678/
                case "talk":
                    _st = Topic(tid=_tid,
                                basedir=self._basedir,
                                dirname=self._dirname
                                ).talk(t, with_file=self._fdown)
                case "solution":
                    # No use.
                    bl4th3r("debug", "Got a `solution`: " + str(t["topic_id"]))
                    _st = ({}, [], [])
                    pass
                case _:  # Any others: task, work, ... Ignore
                    bl4th3r("Debug", "Ignore " + t["type"] + " id: " +
                            str(t["topic_id"]))
                    _st = ({}, [], [])
                    continue  # Start new loop.

            self.topics.append(t["topic_id"])  # Store id, js will find json

            # Todo: Data missing... file info list and image info list.

            try:
                _topic_res_img = _st[0]["images"]
            except KeyError:
                _topic_res_img = []  # Talk with picture, another may not have.

            try:
                _topic_res_files = _st[0]["files"]
            except KeyError:
                _topic_res_files = []  # Talk with file, another may not have.

            if len(_topic_res_img) != 0:
                for _img in _topic_res_img:
                    self.images.append(_img)

            if len(_topic_res_files) != 0:
                for _file in _topic_res_files:
                    self.files.append(_file)

            if _st[1]:
                self.images_link += _st[1]

            if _st[2]:
                self.files_link += _st[2]

            self._cur_idx += 1

            # That's all ?? {talk (answer + digest)}
            bl4th3r("Info", str(self._cur_idx) + "/" +
                    str(self.topic_total) + " processed ...")

        match str(scope).lower():
            case "all":
                # if self.last_topic_idx == self.topic_total:
                if ((self._cur_idx <= topic_max) and (
                        self.topic_total <= topic_max)) or __no_more:
                    bl4th3r("Info",
                            str(self._cur_idx) + " done. " +
                            str(self.topic_total - self._cur_idx) + " hidden.")
                    return self._cur_idx  # <=20 topics, once fetch.
                else:  # recursion, if without any new topic before, len == 0.
                    bl4th3r("Info", "(G) Timerange shift, next page")
                    self.topic(end_time=ztime_before(self.last_update),
                               scope=scope)
            case "digest":
                if self._cur_idx == self.topic_digest or __no_more:
                    return self._cur_idx
                else:  # recursion
                    self.topic(end_time=ztime_before(self.last_update),
                               scope=scope)
            case "answer":
                if self._cur_idx == self.topic_answer or __no_more:
                    return self._cur_idx
                else:  # recursion
                    self.topic(end_time=ztime_before(self.last_update),
                               scope=scope)
            case _:
                bl4th3r("warn", "(G) Content scope not in statistics")
                return self._cur_idx

    def _acquire(self, image_only=False, filetype=None) -> tuple:

        if self.owner_id is None:
            self.topic()
        # Return list of (link, filename) tuple
        if image_only:
            return self.images_link, []

        _flist = []
        if filetype is not None:
            for f in self.files_link:
                if filetype in f[1]:
                    _flist.append(f)
        else:
            _flist = self.files_link

        return self.images_link, _flist

    def jsonify(self) -> tuple:
        """
        Get Group(Channel) information in brief.
        Support call this in anytime, for checking empty value.
        - Not enforcing to get all data. Fetch and fill variables first.
        """

        d = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner_id,
            "topic_count": self.topic_total,
            "topic_count_answer": self.topic_answer,
            "topic_count_digest": self.topic_digest,
            "file_count": self.file_total,
            "topics": self.topics,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "files": self.files,
            "images": self.images,
            # "comments": self.comments  # Comments are saved in topic folders.
        }

        i = {
            "images": self.images,
            "image_task": self.images_link
        }

        f = {
            "files_total": self.file_total,
            "files": self.files,
            "files_task": self.files_link
        }
        if debug:
            bl4th3r("debug",
                    "%G% P0 Topic Object length: " + str(len(d["topics"])))
            bl4th3r("debug",
                    "%G% P1 Downloadable <image>: " + json.dumps(i, indent=2))
            bl4th3r("debug",
                    "%G% P2 Downloadable <file>: " + json.dumps(f, indent=2))

        with open("debug_data.json", 'w') as fd:
            fd.write(json.dumps(d))
        with open("debug_images.json", 'w') as fd:
            fd.write(json.dumps(i))
        with open("debug_files.json", 'w') as fd:
            fd.write(json.dumps(f))

        return d, i, f

    def save(self):
        return self._acquire()

    def __repr__(self):
        return ("{}({!r})".format(self.__class__.__name__, self.id,
                                  self.name, self.description))

    def __hash__(self):
        return self.id

    def __call__(self, *args, **kwargs):
        return self.topic()
