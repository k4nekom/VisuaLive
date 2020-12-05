import json
import re
import requests
import sys

from bs4 import BeautifulSoup
from retry import retry

from apps.app import logger
from .video import Video
from videos.exceptions import VideoNotFound, LiveChatReplayDisabled, ContinuationURLNotFound

class YoutubeVideo(Video):
    def __init__(self, url):
        m = re.search('[0-9A-Za-z-_]{11}', url)
        self.video_id = m.group()

        with open('config/external.json', 'r') as f:
            config = json.load(f)
        self.api_key = config['youtube']['api_key']


    # このメソッドは例外投げます
    def get_info(self):
        url = 'https://www.googleapis.com/youtube/v3/videos'\
              '?id=' + self.video_id + \
              '&key=' + self.api_key + \
              '&part=snippet,contentDetails'
        res = requests.get(url)

        if res.status_code !=200:
            raise(VideoNotFound('動画情報が取得できません'))

        res_dict = json.loads(res.text)

        if res_dict['pageInfo']['totalResults'] == 0:
            raise(VideoNotFound('動画情報が取得できません'))

        # 取得したdurationの単位を「分」に直す
        duration_list = re.findall('[0-9]{1,2}', res_dict['items'][0]['contentDetails']['duration'])
        duration_minutes = int(duration_list[0]) * 60 + int(duration_list[1]) + 1
        video_info = {
            'user_name': res_dict['items'][0]['snippet']['channelTitle'],
            'title': res_dict['items'][0]['snippet']['title'],
            'created_at': res_dict['items'][0]['snippet']['publishedAt'],
            'url': 'https://www.youtube.com/watch?v=' + self.video_id,
            'channel_url': 'https://www.youtube.com/channel/' + res_dict['items'][0]['snippet']['channelId'],
            'duration_minutes': duration_minutes
        }
        return video_info


    def get_comment_data(self):
        try:
            comments = self._get_chat_replay_data()
        except LiveChatReplayDisabled:
            logger.warning(self.video_id + " is disabled Livechat replay")
            raise(VideoNotFound('動画情報が取得できません'))
        except ContinuationURLNotFound:
            logger.warning(self.video_id + " can not find continuation url")
            raise(VideoNotFound('動画情報が取得できません'))
        except Exception:
            logger.warning("Unexpected error:" + str(sys.exc_info()[0]))
            raise(VideoNotFound('動画情報が取得できません'))

        duration_list = re.split(':', comments[-1]['time'])
        # 配信時間が1時間未満の場合 -> 分：秒、1時間以上の場合 -> 時間：分：秒となるため場合分け
        if len(duration_list) == 3:
                duration_minutes = int(duration_list[0]) * 60 + int(duration_list[1]) + 1
        else:
                duration_minutes = int(duration_list[0]) + 1
        comment_count = [0] * duration_minutes
        w_count = [0] * duration_minutes

        for comment in comments:
            commented_time_list = re.split(':', comment['time'])
            # コメント時間が1時間未満の場合 -> 分：秒、1時間以上の場合 -> 時間：分：秒となるため場合分け
            if len(commented_time_list) == 3:
                commented_minute = int(commented_time_list[0]) * 60 + int(commented_time_list[1])
            else:
                # コメント時間がマイナスのコメントは無視
                if commented_time_list[0][0] == '-':
                    continue
                commented_minute = int(commented_time_list[0])

            comment_count[commented_minute] += 1
            # コメントにwがあれば、w_countを増やす
            t = comment['text']
            if len(t) != 0:
                if (t[-1] == 'w') or (t[-1] == 'W') or (t[-1] == 'ｗ') or (t[-1] == 'W') or (t[-1] == '草'):
                    w_count[commented_minute] += 1

        comments_data = {
            'comment_count': comment_count,
            'w_count': w_count
        }
        return comments_data
        

    def _get_chat_replay_data(self):
        youtube_url = "https://www.youtube.com/watch?v="
        target_url = youtube_url + self.video_id
        continuation_prefix = "https://www.youtube.com/live_chat_replay?continuation="
        result = []
        session = requests.Session()
        continuation = self._get_initial_continuation(target_url, session)
        count = 1
        while(1):
            if not continuation:
                break

            try:
                ytInitialData = self._get_ytInitialData(continuation_prefix + continuation, session)
                if not 'actions' in ytInitialData['continuationContents']['liveChatContinuation']:
                    break
                for action in ytInitialData['continuationContents']['liveChatContinuation']['actions']:
                    if not 'addChatItemAction' in action['replayChatItemAction']['actions'][0]:
                        continue
                    chatlog = {}
                    item = action['replayChatItemAction']['actions'][0]['addChatItemAction']['item']
                    if 'liveChatTextMessageRenderer' in item:
                        chatlog = self._convert_chatreplay(item['liveChatTextMessageRenderer'])
                    elif 'liveChatPaidMessageRenderer' in item:
                        chatlog = self._convert_chatreplay(item['liveChatPaidMessageRenderer'])

                    if 'liveChatTextMessageRenderer' in item or 'liveChatPaidMessageRenderer' in item:
                        chatlog['video_id'] = self.video_id
                        chatlog['Chat_No'] = ("%05d" % count)
                        result.append(chatlog)
                        count += 1

                continuation = self._get_continuation(ytInitialData)

            except requests.ConnectionError:
                logger.warning("Connection Error")
                continue
            except requests.HTTPError:
                logger.warning("HTTPError")
                break
            except requests.Timeout:
                logger.warning("Timeout")
                continue
            except requests.exceptions.RequestException as e:
                logger.warning(e)
                break
            except KeyError as e:
                logger.warning("KeyError")
                logger.warning(e)
                break
            except SyntaxError as e:
                logger.warning("SyntaxError")
                logger.warning(e)
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.warning("Unexpected error:" + str(sys.exc_info()[0]))
                logger.warning(e)
                break

        return(result)


    def _get_ytInitialData(self, target_url, session):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        html = session.get(target_url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')

        for script in soup.find_all('script'):
            script_text = str(script)
            if 'ytInitialData' in script_text:
                for line in script_text.splitlines():
                    if 'ytInitialData' in line:
                        return(json.loads(line.strip()[len('window["ytInitialData"] = '):-1]))


    def _get_continuation(self, ytInitialData):
        continuation = ytInitialData['continuationContents']['liveChatContinuation']['continuations'][0].get('liveChatReplayContinuationData', {}).get('continuation')
        return(continuation)


    def _check_livechat_replay_disable(self, ytInitialData):
        conversationBarRenderer = ytInitialData['contents']['twoColumnWatchNextResults']['conversationBar'].get('conversationBarRenderer', {})
        if conversationBarRenderer:
            if conversationBarRenderer['availabilityMessage']['messageRenderer']['text']['runs'][0]['text'] == 'この動画ではチャットのリプレイを利用できません。':
                return(True)


    @retry(ContinuationURLNotFound, tries=3, delay=1)
    def _get_initial_continuation(self, target_url,session):

        ytInitialData = self._get_ytInitialData(target_url, session)

        if self._check_livechat_replay_disable(ytInitialData):
            logger.warning("LiveChat Replay is disable")
            raise LiveChatReplayDisabled

        continue_dict = {}
        continuations = ytInitialData['contents']['twoColumnWatchNextResults']['conversationBar']['liveChatRenderer']['header']['liveChatHeaderRenderer']['viewSelector']['sortFilterSubMenuRenderer']['subMenuItems']
        for continuation in continuations:
            continue_dict[continuation['title']] = continuation['continuation']['reloadContinuationData']['continuation']

        continue_url = continue_dict.get('Live chat repalay')
        if not continue_url:
            continue_url = continue_dict.get('上位のチャットのリプレイ')

        if not continue_url:
            continue_url = continue_dict.get('チャットのリプレイ')

        if not continue_url:
            continue_url = ytInitialData["contents"]["twoColumnWatchNextResults"]["conversationBar"]["liveChatRenderer"]["continuations"][0].get("reloadContinuationData", {}).get("continuation")

        if not continue_url:
            raise ContinuationURLNotFound

        return(continue_url)

    def _convert_chatreplay(self, renderer):
        chatlog = {}

        chatlog['user'] = renderer['authorName']['simpleText']
        chatlog['timestampUsec'] = renderer['timestampUsec']
        chatlog['time'] = renderer['timestampText']['simpleText']

        if 'authorBadges' in renderer:
            chatlog['authorbadge'] = renderer['authorBadges'][0]['liveChatAuthorBadgeRenderer']['tooltip']
        else:
            chatlog['authorbadge'] = ""

        content = ""
        if 'message' in renderer:
            if 'simpleText' in renderer['message']:
                content = renderer['message']['simpleText']
            elif 'runs' in renderer['message']:
                for runs in renderer['message']['runs']:
                    if 'text' in runs:
                        content += runs['text']
                    if 'emoji' in runs:
                        content += runs['emoji']['shortcuts'][0]
        chatlog['text'] = content

        if 'purchaseAmountText' in renderer:
            chatlog['purchaseAmount'] = renderer['purchaseAmountText']['simpleText']
            chatlog['type'] = 'SUPERCHAT'
        else:
            chatlog['purchaseAmount'] = ""
            chatlog['type'] = 'NORMALCHAT'

        return(chatlog)