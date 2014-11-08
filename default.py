#-------------------------------------------------------------------------------
# Name:     plugin.video.miratuserietv
# Purpose:  Plugin para Kodi/XBMC para ver las series del canal miratuserie.tv
#
# Author:      roque.pulido@outlook.com
#
# Created:     07/11/2014
# Copyright:   (c) roque.pulido 2014
# Licence:     GNU GENERAL PUBLIC LICENSE
#-------------------------------------------------------------------------------

import os,urlparse,urllib2,urllib,re,json,sys,plugintools
import xbmc

#variables generales
listaSeries=[]
URLSeries=[]
seriesThums=[]
FANart=""
# Entry point

def run():
    plugintools.log("miratuserie.run")

    # Get params
    params = plugintools.get_params()

    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()
    # Main menu
def main_list(params):
    plugintools.log("miratuserie_tv.main_list "+repr(params))
     #se obtiene lista se series de la pagina
    get_datos()
    ##se obtubieron las series, URL y thumbnail
    #print "-----lista de series, url y thums-------------",listaSeries,URLSeries,seriesThums,"------------------------------"
    for i in range(len(listaSeries)):
        plugintools.add_item(action="temporadas", title=listaSeries[i], url=URLSeries[i], thumbnail=seriesThums[i])
    #(ejemplo de un ulr reprodusible)plugintools.add_item( action="play" , title="test" , plot="es un test" , url="http://94.176.148.101:8777/eupinu2rekie2cbd4mp3vufgdgwp7bczfg5dwpmx6iikuwr5xwxa5b4ovi/v.mp4.flv"  , isPlayable=True, folder=False )

def temporadas(params):
    plugintools.log("miratuserie_tv.temporadas "+repr(params))
    global FANart
    #print "--------------------------------------temporadas------------------------------------"

    data = plugintools.read(params.get("url"))
    FANart = plugintools.find_single_match(data,'<meta property="og:image"  content="(.*?)" >')

    '''
		<li class="temporadas">TEMPORADAS</a></li>
	    <li><a href="/mira-american-horror-story/temporada-1" title="American Horror Story Temporada 1">1</a></li>
	    <li><a href="/mira-american-horror-story/temporada-2" title="American Horror Story Temporada 2">2</a></li>
	    <li><a href="/mira-american-horror-story/temporada-3" title="American Horror Story Temporada 3">3</a></li>
		<li class="random"
    '''
    patron='<li><a href=.*?</a></li>'
    matches = plugintools.find_multiple_matches(data,patron)

    #print "-----------------matches----------------------",matches,"------------------fin marches----------------"
    for match in matches:
        temURL = plugintools.find_single_match(match,'<a href="([^"]+)"')
        temporada=plugintools.find_single_match(match,'title="([^"]+)"')
        url='http://www.miratuserie.tv'+temURL
        plugintools.add_item(action="capitulos", title=temporada, url=url,thumbnail="", fanart=FANart)

def capitulos(params):
    plugintools.log("miratuserie_tv.capitulos "+repr(params))

    #print"-----------------fanart------------------------",params.get("info_labels"),"--------------------------"
    #print "--------------------------------------capitulos------------------------------------"
    data=plugintools.read(params.get("url"))

    patron='<div class="capitulo">(.*?)</div>'
    matches = plugintools.find_multiple_matches(data,patron)
    #print "-----------------matches----------------------",matches,"------------------fin marches----------------"
    for match in matches:
        url=plugintools.find_single_match(match,'<a href="([^"]+)"')
        nombre=plugintools.find_single_match(match,'<h3 class="titulo">(.*?)</h3>')
        descipcion=plugintools.find_single_match(match,'<p class="desc">(.*?)</p>')
        imagen=plugintools.find_single_match(match,'<img src="(.*?)"')
        print "------------------------------------",url,nombre,descipcion,imagen,params,"--------------------------------------------------"
        plugintools.add_item(action="servidores", title=nombre, url=url, thumbnail=imagen,plot=descipcion)


def servidores(params):
    plugintools.log("miratuserie_tv.servidores "+repr(params))
    data=plugintools.read(params.get("url"))
    urlservidores=plugintools.find_single_match(data,'<iframe class="servidores" src="([^"]+)"')
    urlser="http://www.miratuserie.tv"+urlservidores
    plugintools.add_item(title=urlser,folder=False)#linea para monitoriar variable
    pagservidores=plugintools.read(urlser)
    #print "---------------------------------Imprimiendo pagina-------------------------------------------",pagservidores,"---------------------------------------------------------------------------"
    subnum=plugintools.find_single_match(pagservidores,'tc:(.*?),')
    iniciourl=plugintools.find_single_match(pagservidores,"url: '(.*?)'")
    calidadN=plugintools.find_single_match(pagservidores,'<div id="servidoresN">(.*?)</div>')
    CalidadHD=plugintools.find_single_match(pagservidores,'<div id="servidoresHD">(.*?)</div>')
    #print "---------------------------------Imprimiendo calidad N-------------------------------------------",calidadN,"---------------------------------------------------------------------------"
    #print "---------------------------------Imprimiendo CalidadHD-------------------------------------------",CalidadHD,"---------------------------------------------------------------------------"
    #print "---------------------------------Imprimiendo subnum-------------------------------------------",subnum,"---------------------------------------------------------------------------"
    #print "---------------------------------Imprimiendo iniciourl-------------------------------------------",iniciourl,"---------------------------------------------------------------------------"

    patron='<a href="#"(.*?)</a>'
    matchesN = re.compile(patron,re.DOTALL).findall(calidadN)
    matchesHD = re.compile(patron,re.DOTALL).findall(CalidadHD)

    #print "---------------------------------Imprimiendo matchesN------------------------------------------",matchesN,"---------------------------------------------------------------------------"
    #print "---------------------------------Imprimiendo matchesHD-------------------------------------------",matchesHD,"---------------------------------------------------------------------------"
    plugintools.add_item(title="[COLOR blue][B]Calidad Estandar[/B][/COLOR]",folder=False)


    for match in matchesN:
        nombre=plugintools.find_single_match(match,'<img alt="([^"]+)"')
        imagen="http:"+plugintools.find_single_match(match,'src="([^"]+)"')
        url=plugintools.find_single_match(match,'onclick="([^"]+)"')+' sub="'+subnum+'" urlorg="'+iniciourl+'"'
        #print "------------------------------------variables obtenidas nombre", nombre,"imagen",imagen,"url",url,"-----------------------"
        plugintools.add_item(action="play",title=nombre,thumbnail=imagen,url=url,isPlayable=True, folder=False)

    plugintools.add_item(title="[COLOR blue][B]Calidad HD[/B][/COLOR]",folder=False)

    for match in matchesHD:
        nombre=plugintools.find_single_match(match,'<img alt="([^"]+)"')
        imagen="http:"+plugintools.find_single_match(match,'src="([^"]+)"')
        url=plugintools.find_single_match(match,'onclick="([^"]+)"')
        #print "------------------------------------variables obtenidas nombre", nombre,"imagen",imagen,"url",url,"-----------------------"
        plugintools.add_item(action="play",title=nombre,thumbnail=imagen,url=url,isPlayable=True, folder=False)

def video(params):
    plugintools.log("miratuserie_tv.video "+repr(params))
    url=params.get("url")
    plugintools.add_item(title=url)
    #"verVid('kv2a6a98x113','played',0,1,0,1,'es'); sub="112" urlorg="americanhorrorstory/ir""
    #url ="verVid('kv2a6a98x113','played',0,1,0,1,'es'); sub='112' urlorg='americanhorrorstory/ir'"
    id=plugintools.find_single_match(url,"verVid\((.*?)\);")
    split1= plugintools.find_multiple_matches(id,"'(.*?)'")
    split2= plugintools.find_multiple_matches(id,",(\d)")
    #spliit1 [0] key ,[1]host,[2]idiomas
    #split2 [0]plugin,[1]subs,[2]hd,[3]gk
    sub= plugintools.find_single_match(url,'sub="(.*?)"')
    urlorig= plugintools.find_single_match(url,'urlorg="(.*?)"')
    #print sub
    #print urlorig
    key=split1[0]
    host=split1[1]
    plugin=split2[0]
    subs=split2[1]
    sub=sub
    hd=split2[2]
    gk=split2[3]
    idiomas=split1[2]
    urlserie=urlorig
    urlvideo=get_url_video(key,host,plugin,subs,sub,hd,gk,idiomas,urlserie)
    #print "--------split------",split1,"--------split2------",split2
    #print key,host,plugin,subs,sub,hd,gk,idiomas,urlserie,urlvideo
    pagvideo=plugintools.read(urlvideo)
    print "-----------------------pagvideo----------------------------------",pagvideo,"-----------------------------------------------"

def play(params):
    url="http://89.238.150.152:8777/wupymmluk2ie2cbd4m435f5aalojml6xavbsuouby664djmvb6h6edclbi/v.mp4.flv"
    urlsub="http://sc.miratuserie.tv/americanhorrorstory/subs/404.srt"
    player=xbmc.Player()

    plugintools.play_resolved_url(url) #(reproduce el video)
    player.setSubtitles(urlsub)



def get_url_video(key,host,plugin,subs,sub,hd,gk,idiomas,urlserie):
    plugintools.log("miratuserie_tv.get_url_video ")
    key=key
    host=host
    plugin=plugin
    subs=subs
    tc=sub  #908
    hd=hd
    gk=gk
    idiomas=idiomas
    urlserie=urlserie
    params=urllib.urlencode({"key":key,"host":host,"plugin":plugin,"subs":subs,"tc":sub,"hd":hd,"gk":gk,"idiomas":idiomas})
    f=urllib2.urlopen("http://www.miratuserie.tv/"+urlserie,params)
    urlvideo=f.read()
    f.close()
    print "------------urlvideo---------",urlvideo,"--------------------"
    return urlvideo



def get_datos():
    pagina = plugintools.read("http://miratuserie.tv/lista.json") #Obitiene el Json con la lista de series y URL
    varJson= json.loads(pagina)
    for i in range(len(varJson)):
        if i==18:
            listaSeries.append("Escobar, El Patron del Mal")
            URLSeries.append('http://www.miratuserie.tv/mira-'+varJson[i]["url"])
            seriesThums.append('http://sc.miratuserie.tv/posters/'+varJson[i]["url"]+".jpg")
        else:
            listaSeries.append(varJson[i]["value"])
            URLSeries.append('http://www.miratuserie.tv/mira-'+varJson[i]["url"])
            seriesThums.append('http://sc.miratuserie.tv/posters/'+varJson[i]["url"]+".jpg")


run()
