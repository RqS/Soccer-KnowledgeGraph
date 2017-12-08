from bs4 import BeautifulSoup
import re
import codecs
import sys
import json

f = codecs.open(sys.argv[1])
output = codecs.open(sys.argv[2], "w")
# f = codecs.open("test.jl")
ii=0

pattern = re.compile("https:\/\/www.reddit.com\/r\/soccerdiscussions\/comments\/[^\/]*/[^\/]*/$")

for line in f:
    data = json.loads(line)

    url = data["url"]
    print url
    print ii
    ii += 1
    if not pattern.match(url):
        fake_html = u"<!doctype html><html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en-us\" xml:lang=\"en-us\"><head></head><body>"
        html_doc = data["raw_content"]
        soup = BeautifulSoup(html_doc, 'html.parser')

        if soup.find("div", {"class": "sitetable nestedlisting"}):
            text_divs = soup.find("div", {"class": "sitetable nestedlisting"})
            fake_html = str(text_divs).decode('utf-8') + u"</body></html>"
            data['comments'] = text_divs.text

        if soup.find("div", {"class": "top-matter"}):
            topic = soup.find("div", {"class": "top-matter"})
            data["topic"] = topic.p.a.text
        
        data['fake_html'] = fake_html
              
        # data["knowledge_graph"] = profile
        json.dump(data, output)
        output.write("\n")

f.close()
output.close()



