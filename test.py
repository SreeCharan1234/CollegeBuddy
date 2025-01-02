from youtube_transcript_api import YouTubeTranscriptApi
def get_transcript(video_url):

  
  video_id = video_url.split("=")[1]

  
  transcript_api = YouTubeTranscriptApi()

  
  transcript = transcript_api.get_transcript(video_id)
  st.write(transcript)

  return transcript

get_transcript("https://www.youtube.com/watch?v=YaEG2aWJnZ8")