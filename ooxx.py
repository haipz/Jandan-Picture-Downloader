'''

    author  : haipz
    site    : haipz.com
    email   : i@haipz.com

modified by TC
oo xx indexes are included.

'''

import urllib2, os, re, thread, time

def getHtml(url) :
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    html = page.read()
    return html

def filterComment(source) :
    pattern = ur'begin comments([\s\S]*?)end comments'
    matchs = re.search(pattern, source)
    return matchs.group()

def filterThumbnail(source) :
    pattern = ur'<img src="([\s\S]*?)\.gif"'
    reobj = re.compile(pattern)
    result, number = reobj.subn('', source)
    return result

def downloadPicture(picurl, picpath, picname) :
    pic = urllib2.urlopen(picurl)
    f = open(picpath + picname, 'wb')
    f.write(pic.read()) 
    f.close()
    print 'System: ' + picname + ' saved\n'

choice = int(input("0. ooxx 1. pic : "))
pagestart = int(input("page start: "))
pageend = int(input("page end: "))
ooover = int(input("at least how many oo: "))
xxbelow = int(input("at most how many xx: "))

if choice == 0 :
    dirname = "ooxx"
else :
    dirname = "pic"

path = os.getcwd() + "/" + dirname
isExists = os.path.exists(path)
if not isExists :
    print 'System: ' + path + " created"
    os.makedirs(path)
else :
    print 'System: ' + path + " exists"

initurl = "http://jandan.net/" + dirname + "/"

for pagenum in range(pagestart, pageend) :
    cururl = initurl + "page-" + str(pagenum)
    print 'Current url: ' + cururl
    inithtml = getHtml(cururl)
    curhtml = filterComment(inithtml)

    pattern = ur'<li id="comment-([\s\S]*?)</li>'
    reobj = re.compile(pattern)
    matchs = reobj.findall(curhtml)
    count0 = 0
    for match in matchs :
        count0 = count0 + 1
        match = filterThumbnail(match)

        oopattern = ur'(?:<span id="cos_support-)(?:\d*?)(?:">)(\d*?)(?:</span>)'
        xxpattern = ur'(?:<span id="cos_unsupport-)(?:\d*?)(?:">)(\d*?)(?:</span>)'
        oo = re.search(oopattern, match).group(1)
        xx = re.search(xxpattern, match).group(1)

        picpattern = ur'(?:href=")(http\:\/\/w[\s\S]*?)(.jpg|.png|.gif)'
        picobj = re.compile(picpattern)
        result = picobj.findall(match)

        count1 = 0
        for pic in result :
            if int(oo) > ooover and int(xx) < xxbelow:
                count1 = count1 + 1
                picurl = pic[0] + pic[1]
                picpath = path + '/'
                picname = str(pagenum) + '_oo' + oo + '_xx' + xx + '_' + str(count0) + '_' + str(count1) + pic[1]

                print 'Infomation:'
                print 'Picture url: ' + picurl
                print 'Picture path: ' + picpath
                print 'Picture name: ' + picname
                try :
                    downloadPicture(picurl, picpath, picname)
                except Exception as e :
                    print(e)
