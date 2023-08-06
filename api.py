"""This file belongs to project 'LIGHTPARTICLE', See README for more detail."""

#  This is not a standalone executable module.

from utility import ztime


# ### Maintainer(s): _3083 ###
# 2023-07-28    v0.1 Code Review - 1st.
#                   - Add documents (PEP-8 / PEP-257)
#                   - Fix time filter check.
#                   - Move file link query from conn to API.
#                   - Fix typo and builtins name.
#                   - Add new function of downlink exceed check.


class API(object):
    """
    Mockup any link of resource.
    ---

    """
    VER = 2
    HOST = "https://api.zsxq.com"

    def __init__(self, host="https://api.zsxq.com", version=2):
        """
        API constructor. Support domain and API version upgrade.

        Parameters:
            host:<str>      Target API domain
            version:<int>   Version of API service
        """
        self.h = host
        API.HOST = self.h  # Override if domain changed.

        self.v = version
        API.VER = self.v

    @staticmethod
    def _time_filter(p, begin_time, end_time):
        """
        Check time range was specified or not.

        Parameters:
            begin_time:<zTimeStr>       Time range of beginning.
            end_time:<zTimeStr>         End timestramp of time range.
        """
        if isinstance(begin_time, str) and isinstance(end_time, str):
            if (begin_time is not None) and (end_time is not None):
                if (ztime(end_time) - ztime(begin_time)).seconds > 0:
                    pass
                else:
                    return p

            if end_time is not None:
                p.extend(["&end_time=", end_time])

            if begin_time is not None:  # Unusual parameter. (Beta)
                p.extend(["&begin_time=", begin_time])

        return p

    @classmethod
    def user(cls, uid=None):
        """
        Provide test url (self session ID), user info.

        Parameters:
            uid:<int>       unique id of account user (Your login)
        """
        _endpoint = ["/v" + str(API.VER), "/users"]
        if uid is None:
            _endpoint.append("/self")
        else:
            _endpoint.append("/" + str(uid))
        return API.HOST + ''.join(_endpoint)

    @classmethod
    def comment(cls, topic_id, sort="asc", count=30, sticky=True,
                end_time=None, begin_time=None):
        """
        Get comment within a topic (With TopicID)

        Parameters:
            topic_id:<int>          Topic unique id.
            sort:<str>              Sort direction.
            count:<int>             Counts of comment every request
            sticky:<bool>           Get comment with sticky mode. (True dfl.)
            begin_time:<zTimeStr>   Time range filter - begin
            end_time:<zTimeStr>     Time range filter - end

        :sort:
            - asc
            - desc
        """
        p = ["/v" + str(API.VER), "/topics", '/', str(topic_id), "/comments?",
             "sort=", sort, "&count=", str(count)]

        if sticky:
            p.extend(["&with_sticky=", str(sticky).lower()])

        p = API._time_filter(p, begin_time, end_time)

        return API.HOST + ''.join(p)

    @classmethod  # Override (with time range
    def topic_list(cls, group_id, scope="all", count=20,
                   end_time=None, begin_time=None):
        """
        Get topic list.

        Parameters:
            group_id:<int>          Unique id of group.
            scope:<str>             Content type filter.
            count:<int>             Counts of file.
            begin_time:<zTimeStr>   Time range filter - begin
            end_time:<zTimeStr>     Time range filter - end

        :scope:
            - all
            - digests
            - by_owner
            - questions
            - tasks
            - with_files
            - with_images

        * The param `begin_time` is not usual.
        """
        p = ["/v" + str(API.VER), "/groups", '/', str(group_id), "/topics?",
             "scope=", str(scope).lower(), "&count=", str(count)]

        if end_time is not None:
            p.extend(["&end_time=", end_time])

        if begin_time is not None:  # Unusual parameter. (Beta)
            p.extend(["&begin_time=", begin_time])

        return API.HOST + ''.join(p)

    @classmethod
    def group_info(cls, group_id):
        """
        Get group description.

        Parameters:
            group_id:<int>      Group unique id.
        """
        p = ["/v" + str(API.VER), "/groups", "/", str(group_id)]
        # This API without any parameters!
        return API.HOST + ''.join(p)

    @classmethod
    def file(cls, group_id, file_count=3, begin_time=None,
             end_time=None) -> str:
        """
        Get All files details.

        Parameters:
            group_id:<int>          Group unique id.
            file_count:<int>        Count of files every request.
            begin_time:<zTimeStr>   Time range filter - Start of time.
            end_time:<zTimeStr>     Time range filter - End of time.

        * The param `begin_time` is not usual.
        """
        p = ["/v" + str(API.VER), "/groups", '/', str(group_id), "/files?",
             "&count=" + str(file_count)]

        p = API._time_filter(p, begin_time, end_time)

        return API.HOST + ''.join(p)

    @classmethod
    def columns(cls, group_id, summary=False):
        """
        Get All columns (Zhuan-Lan)
        eg. /v2/groups/12345678/columns/summary

        Parameters:
            group_id:<int>      Group unique id.
            summary:<bool>      Only get brief data.
        """
        resource = ["/v" + str(API.VER), "/groups", "/", str(group_id),
                    "/columns"]
        if summary:
            resource.append("/summary")

        return API.HOST + ''.join(resource)

    @classmethod
    def columns_topic(cls, group_id, count=100,
                      sort="attached_to_column_time", direction="desc"):
        """
        Get sub-columns with group-id and column-id.

        Parameters:
            group_id:<int>      Group unique id.
            count:<int>         Counts of topic that we query.
            sort:<str>          Sort method name.
            direction:<str>     Direction of sorted content.

        :sort:
            - attached_to_column_time
            - create_time
        :direction:
            - desc
            - asc

        """
        resource = ["/v" + str(API.VER), "/groups", "/", str(group_id),
                    "/columns/topics?", "count=", str(count), "&sort=", sort,
                    "&direction=", direction]

        return API.HOST + ''.join(resource)

    #
    # === All links below were generated without group id. ===
    #

    @classmethod
    def group_list(cls):
        """
        Get user paid group id list.
        /v2/groups
        """
        return API.HOST + ''.join(["/v" + str(API.VER), "/groups"])

    @classmethod
    def file_link(cls, fileid):
        """
        Get the file resource downlink

        Parameters:
            fileid:<int>        File attachment unique id.
        """

        if isinstance(fileid, tuple):
            fileid = fileid[0]  # TODO: Trace and fix dirty link mock.

        resource = ["/v" + str(API.VER), "/files", '/', str(fileid),
                    "/download_url"]

        return API.HOST + ''.join(resource)

    @classmethod
    def topic_info(cls, topic_id):
        """
        Get Topic details.
        example: /v2/topics/1234567890987654/info

        Parameters:
            topic_id:<int>      Topic unique id.
        """
        resource = ["/v" + str(API.VER), "/topics", "/", str(topic_id), "/info"]

        return API.HOST + ''.join(resource)
