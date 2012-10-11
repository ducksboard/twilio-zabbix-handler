from xml.sax import saxutils

from twisted.web import resource


class AlertTwiML(resource.Resource):

    isLeaf = True

    HANGUP = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Hangup/>
</Response>
"""

    SAY = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">Alert! %s</Say>
    <Hangup/>
</Response>
"""

    def render_GET(self, request):
        output = ''
        try:
            message = self.extract_message(request)
        except Exception, e:
            output = self.HANGUP
        else:
            output = self.generate_say(message)

        request.setHeader('Content-Type', 'application/xml')
        request.setHeader('Content-Length', len(output))
        return output

    render_POST = render_GET

    def extract_message(self, request):
        subject = request.args["subject"][0]
        if subject.startswith("ALERT:"):
            subject = subject[len("ALERT:"):]

        subject = subject.strip()
        return subject

    def generate_say(self, message):
        return self.SAY % saxutils.escape(message)


resource = resource.Resource()
resource.putChild("", AlertTwiML())
