import pycurl, json, base64, StringIO, sys
import ConfigParser, os

class Slack:
	def __init__(self):
		settings = ConfigParser.ConfigParser()
		settings.read('settings.ini')
		self.domain = settings.get('settings', 'domain')
		self.token = settings.get('settings', 'token')

	def post(self,channel='dev', text='--', username='Slacker',icon_url='http://hs.findingapogee.com/publicfiles/fahomei.png'):
		payload = {
			"channel":"#" + channel,
			"text":text,
			"username":username,
			"icon_url":icon_url
		}
		call = self._apiCall(payload)
		return call
		
	def _apiCall (self, payload):
		# this.options.payload = Utilities.jsonStringify(this);
		# this.response = UrlFetchApp.fetch(this.api+'?token='+this.token, this.options).getContentText();
		api_url = 'https://' + self.domain + '.slack.com/services/hooks/incoming-webhook?token=' + self.token
		
		print api_url
		curl = pycurl.Curl()
		curl.setopt(curl.HTTPHEADER, [
			'Content-Type: application/json'
		])
		curl.setopt(curl.URL, api_url)
		curl.setopt(curl.POSTFIELDS, json.dumps(payload))
		curl.setopt(curl.VERBOSE, True)
		contents = StringIO.StringIO()
		curl.setopt(pycurl.WRITEFUNCTION, contents.write) 
		curl.perform()
		self.response = contents.getvalue()
		return self.response
		
bam = Slack()
print len(sys.argv)
def usage():
	print('usage: channel text username icon_url')
	print('Example: general "This is my message" "Bugs Bunny" "http://example.com/img.png')
	
# confirm proper arguments		
if sys.argv[1] == 'help':
	usage()
	sys.exit
	
if len(sys.argv) == 3:
	bam.post(channel=sys.argv[1],text=sys.argv[2])
elif len(sys.argv) == 4:
	bam.post(channel=sys.argv[1],text=sys.argv[2],username=sys.argv[3])
elif len(sys.argv) == 5:
	bam.post(channel=sys.argv[1],text=sys.argv[2],username=sys.argv[3],icon_url=sys.argv[4])
else:
	usage()
	
print bam.response


