import requests

# 참고 사이트: https://developerdk.tistory.com/96


def dm(channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={
                                 "Authorization": "Bearer xoxb-1682940574129-1994341974995-33rdNAP3ePMUjFSyOF2E0eFV"},
                             data={"channel": channel, "text": text}
                             )

    return response
