from getpass import getpass
from argparse import ArgumentParser, Namespace
from typing import Union

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_apikey_service():
	api_key = getpass("Google API key: ")
	return build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)

def youtube_search(options: Union[dict, Namespace]):
	youtube = get_apikey_service()
	print(type(options))
	search_args = dict(part='id,snippet', order='date')

	if type(options) is Namespace:
		options = vars(options)
	search_args.update(options)

	search_response = youtube.search().list(**search_args).execute()

	videos = []
	channels = []
	playlists = []
	
	for search_result in search_response.get('items', []):
		if search_result['id']['kind'] == 'youtube#video':
			videos.append({
				'title': search_result['snippet']['title'],
				'video_id':search_result['id']['videoId']
			})
		elif search_result['id']['kind'] == 'youtube#channel':
			channels.append({
				'title': search_result['snippet']['title'],
				'channel_id': search_result['id']['channelId']
			})
		elif search_result['id']['kind'] == 'youtube#playlist':
			playlists.append({
				'title': search_result['snippet']['title'],
				'playlist_id': search_result['id']['playlistId']
			})

	return {
		'videos': videos,
		'channels': channels,
		'playlists': playlists
	}

def get_channel_videos(channel_id: int, max_results: int = 20):
	args = {"channelId": channel_id, "maxResults": max_results}
	res = youtube_search(args)
	return res

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("--channelId", help="Channel ID", required=True)
	parser.add_argument("--maxResults", help="Max no. results to show.", default=20)

	args = parser.parse_args()

	try:
		res = youtube_search(args)
		print(res)
	except HttpError as e:
		print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')