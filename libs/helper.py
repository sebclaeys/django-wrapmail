__author__ = 'sebastienclaeys'

class DummyRecipient(object):
    def __init__(self, email, fields={}):
        self.email = email
        for key, val in fields.iteritems():
            self.__dict__[key] = val



import common.libs.html2text as html2text
#from BeautifulSoup import BeautifulSoup

def html_to_text(html_content):
    h = html2text.HTML2Text()
    h.ignore_images = True
    #text_content = BeautifulSoup(html_content).getText().replace('\n','<br>')
    return h.handle(html_content)

# Process the events and call the given callback if exists for each event
def process_events(callback=None):
    import mailator.models as model
    for event in model.Event.objects.filter(processed=False):
        email = event.email

        # Mark bounce and spam as no_send
        if event.event == 'bounce':
            r = model.Recipient.objects.filter(email=email)
            if r:
                r = r[0]
                r.no_send = True
                r.save()

        if callback:
            callback(event)

        event.processed = True
        event.save()
