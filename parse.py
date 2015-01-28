
import web
import urllib

class ParseHtml():
    Decode_JS = '''
    function HTMLDecode ( input )
    {
    var converter = document.createElement("DIV");
    converter.innerHTML = input;
    var output = converter.innerText;
    converter = null;
    return output;
    }
    '''
    Encode_JS = '''
    function HTMLEncode ( input )
    {
    var converter = document.createElement("DIV");
    converter.innerText = input;
    var output = converter.innerHTML;
    converter = null;
    return output;
    }
    '''

    Token = '8c100cd4b9d627f58a844b7188e1a8275907f02a'

    def GET(self):
        url = web.input().get("url")
        parseurl_api = 'https://www.readability.com/api/content/v1/parser?url='+url+'&token='+self.Token
        parse_json = urllib.urlopen(url).read()
        try:
            content = parse_json
        except Exception as ex:
            return ex
        return content


