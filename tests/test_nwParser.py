from unittest import TestCase
from nw.parser import NwParser
from nw.beat import *
from bs4 import BeautifulSoup


class TestNwParser(TestCase):
    def setUp(self):
        self.topic_html_no_quotes = '<!DOCTYPE html>\n<html>\n<head>\n\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n        <link rel="SHORTCUT ICON" href="http://netwars.pl/favicon.ico" />\n\t<title>Prezenty na święta - 2016</title>\n\t\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js" type="text/javascript" language="javascript"></script>\n<link rel="stylesheet" type="text/css" media="all" href="http://netwars.pl/style-new3.css"/>\t<script language="javascript" type="text/javascript">\n<!--\n\n\n        function HideMenu() {\n                $("#topic_173472 .post_menu").remove();\n        }\n\n        function FadeMenu() {\n            return setTimeout(function(){\n                                 HideMenu();\n                             }, 2000 );\n        }\n\n        function ToggleMenu (post_id) {\n                var is_already = $("#"+post_id+" div").hasClass("post_menu");\n                HideMenu();\n                if (!is_already) {\n                       var topic_header = $("#"+post_id+" .posthead");\n                       var user_id = post_mapper[post_id];\n\n                       var menu = [];\n\n                       if (user_id == owner_id) {\n                               // menu.push(\'<a name="edit">Edytuj</a>\');\n                       } else {\n                            if (user_mapper.hasOwnProperty("user_"+user_id)) {\n                                menu.push(\'<a name="unignore">Przestań ignorować</a>\');\n                                if ($("#"+post_id+" .post_body").is(":visible")) {\n                                    menu.push(\'<a name="ighide">Ukryj</a>\');\n                                } else {\n                                    menu.push(\'<a name="igshow">Pokaż</a>\');\n                                }\n                            } else {\n                                menu.push(\'<a name="ignore">Ignoruj użytkownika</a>\');\n                            }\n                            menu.push(\'<a name="unreaded">Oznacz jako nieprzeczytane</a>\');                            \n                       }\n                            topic_header.after(\'<div class="post_menu">\'+menu.join(\' | \')+\'<span class="error"></span></div>\');\n                }\n        }\n\n        function RefreshIgnore(user_id) {\n              var ignored = (user_mapper.hasOwnProperty("user_"+user_id));\n              for (var elem in post_mapper) {\n                    if (post_mapper[elem] === user_id) {\n                        if (ignored) {\n                             $("#"+elem+" .post_body").hide();\n                             $("#"+elem+" .ignored").remove();\n                             $("#"+elem+" .p2_nick .nick").after(\' <span class="ignored">I</span>\');\n                        } else {\n                             $("#"+elem+" .post_body").show();\n                             $("#"+elem+" .ignored").remove();\n                        }\n                    }\n              }\n        }\n\n        $().ready(function(){\n             $("#topic_173472").on("click",".post_body a.cite_link",function(event){\n                event.preventDefault();\n                var owen = $(this).parent().children(".cite_field");\n                if (owen.is(":visible")) {\n                      owen.hide().empty();\n                      $(this).html("[Pokaż]");\n                } else {\n                      var name = $(this).parent().attr("name");\n                      var wynik = $("#"+name).clone().removeAttr("id");\n                      wynik.children(".cite").children(".cite_field").hide().empty().end().children(".cite_link").html("pokaz");\n                      $(owen).show().append(wynik);\n                      $(this).html("[Schowaj]");\n                }\n             });\n         });\n$(document).ready(function(){\n // I added the video size here in case you wanted to modify it more easily\n var vidWidth = \'100%\';\n var vidHeight = \'400\';\n\n var showYoutube = "<a class=\'shower\' href=\'#\' onClick=\'$(this).parent(\\"div\\").find(\\"object\\").show(); $(this).parent(\\"div\\").find(\\".hider\\").show(); $(this).hide(); return false;\'>[Pokaż film]</a>";\n var hideYoutube = "<a style=\'display: none\' class=\'hider\' href=\'#\' onClick=\'$(this).parent(\\"div\\").find(\\"object\\").hide(); $(this).parent(\\"div\\").find(\\".shower\\").show(); $(this).hide(); return false;\'>[Schowaj film]</a><br />";\n\n var obj = \'<div class="cite">\' + showYoutube + hideYoutube + \'<object style="display: none" width="\' + vidWidth + \'" height="\' + vidHeight + \'">\' +\n     \'<param name="movie" value="http://www.youtube.com/v/[vid]&hl=en&fs=1">\' +\n     \'</param><param name="allowFullScreen" value="true"></param><param \' +\n     \'name="allowscriptaccess" value="always"></param><em\' +\n     \'bed src="http://www.youtube.com/v/[vid]&hl=en&fs=1" \' +\n     \'type="application/x-shockwave-flash" allowscriptaccess="always" \' +\n     \'allowfullscreen="true" width="\' + vidWidth + \'" \' + \'height="\' +\n     vidHeight + \'"></embed></object></div> \';\n\n $(\'a[href*="youtube.com/watch"]\').each(function(){\n  var that = $(this);\n  var vid = that.attr(\'href\').match(/(?:v=)([\\w\\-]+)/g); // end up with v=oHg5SJYRHA0\n  if (vid.length) {\n   $.each(vid, function(){\n    that.after( obj.replace(/\\[vid\\]/g, this.replace(\'v=\',\'\')) );\n   });\n  }\n });\n});\n\nvar owner_id = -1\nvar topic_id = 173472\nvar topic_observed = 0\nvar post_mapper = {"post_1":"30794","post_2":"31718","post_3":"27527","post_4":"18877","post_5":"10647","post_6":"18877","post_7":"31718","post_8":"30794","post_9":"27527","post_10":"18877","post_11":"31840","post_12":"29977","post_13":"9926","post_14":"19476","post_15":"28123","post_16":"21818","post_17":"31840"}\nvar user_mapper = {}\n// -->\n</script></head>\n<body>\n\n<div id="strona">\n\n\t<div id="logo">\n            <a href="http://www.pajacyk.pl" target="_blank">\n\t\t<img src="http://netwars.pl/images//pajacyk2.jpg"></a>\n\t</div>\n\t\n\t<div id="main">\n\t\t<center><a href="http://netwars.pl/temat/143798"><b>NETWARS - CZĘSTO ZADAWANE PYTANIA</b></a></center>\n        <div class="login_box"><form action="/login" method="post"><input type="hidden" name="redir" value="/temat/173472">Nick: <input type="text" name="tnick" size="12"> Hasło: <input type="password" name="tpass" size="8"> <input type="submit" value="Zaloguj"></form> <a href="/register">Załóż konto</a> | <a href="/recover">Przypomnij hasło</a><BR/> </div><br />\n        <b><a href=#footer>Zjedź na dół</a></b><BR /><BR /><ul class="forum_navi"><li><a href="/forum">Forum</a>&nbsp;&gt;&gt;&nbsp;</li><li><a href="/forum/4">OT</a>&nbsp;&gt;&gt;&nbsp;</li><li>Prezenty na święta - 2016</li></ul><div id="topic_173472"><div class="post" id="post_1"><div class="posthead"><div class="p2_data">Wczoraj, 21:26:19</div><div class="p2_nick"><span class="numerek_posta">[#1]</span>&nbsp;<a class="nick" href="/user/30794">NFS2</a></div></div><div class="post_body">Hej, jak co roku nadchodzą swięta i trzeba kupić prezenty. <br />\r\nMacie już coś upatrzonego - co kupujecie ? <br />\r\nTemat inspiracyjny - bo obecnie brak pomysłów - co kupić</div></div><div class="post" id="post_2"><div class="posthead"><div class="p2_data">Wczoraj, 21:31:08</div><div class="p2_nick"><span class="numerek_posta">[#2]</span>&nbsp;<a class="nick" href="/user/31718">Rybakus</a></div></div><div class="post_body">Nadchodzą święta... Człowieku jeszcze ponad miesiąc...</div></div><div class="post" id="post_3"><div class="posthead"><div class="p2_data">Wczoraj, 21:31:20</div><div class="p2_nick"><span class="numerek_posta">[#3]</span>&nbsp;<a class="nick" href="/user/27527">Oscar</a></div></div><div class="post_body">skarpety i bokserki</div></div><div class="post" id="post_4"><div class="posthead"><div class="p2_data">Wczoraj, 21:32:55</div><div class="p2_nick"><span class="numerek_posta">[#4]</span>&nbsp;<a class="nick" href="/user/18877">MCh)ZbeeR</a></div></div><div class="post_body">skarpety i pomarańcze</div></div><div class="post" id="post_5"><div class="posthead"><div class="p2_data">Wczoraj, 21:32:55</div><div class="p2_nick"><span class="numerek_posta">[#5]</span>&nbsp;<a class="nick" href="/user/10647">Zylcu</a></div></div><div class="post_body">Jak #3 + jakies mandarynki/pomarancze</div></div><div class="post" id="post_6"><div class="posthead"><div class="p2_data">Wczoraj, 21:33:21</div><div class="p2_nick"><span class="numerek_posta">[#6]</span>&nbsp;<a class="nick" href="/user/18877">MCh)ZbeeR</a></div></div><div class="post_body">xD</div></div><div class="post" id="post_7"><div class="posthead"><div class="p2_data">Wczoraj, 21:34:08</div><div class="p2_nick"><span class="numerek_posta">[#7]</span>&nbsp;<a class="nick" href="/user/31718">Rybakus</a></div></div><div class="post_body">Dla kobiety też skarpety, bokserki i pomarańcze?</div></div><div class="post" id="post_8"><div class="posthead"><div class="p2_data">Wczoraj, 21:38:08</div><div class="p2_nick"><span class="numerek_posta">[#8]</span>&nbsp;<a class="nick" href="/user/30794">NFS2</a></div></div><div class="post_body">heh :&lt; tematy z ubiegłych lat były ciekawsze... moze ktos cos normalnie napisz ?<p class="post_modified">Zmieniony Wczoraj, 21:38:45 przez NFS2</p></div></div><div class="post" id="post_9"><div class="posthead"><div class="p2_data">Wczoraj, 21:38:59</div><div class="p2_nick"><span class="numerek_posta">[#9]</span>&nbsp;<a class="nick" href="/user/27527">Oscar</a></div></div><div class="post_body">jeszcze orzechy</div></div><div class="post" id="post_10"><div class="posthead"><div class="p2_data">Wczoraj, 21:39:25</div><div class="p2_nick"><span class="numerek_posta">[#10]</span>&nbsp;<a class="nick" href="/user/18877">MCh)ZbeeR</a></div></div><div class="post_body"><div class="cite" name="post_8">W 8 NFS2 napisał: <a href="#" class="cite_link">[Pokaż]</a>\n                      <div class="cite_field"></div>\n                 </div> No dobra, chcesz konkretnych propozycji to Ci pomoge:<br />\r\n<br />\r\nKup żonie wibrator<br />\r\n<br />\r\n<br />\r\n<br />\r\n<br />\r\nBo jeśli byś miał jaja i kutasa w spodniach, to byś znał swoich bliskich, skąd my mamy wiedziec co Twoja rodzina lubi? Powiem Ci abyś kupił siostrzenicy hulajnoge, a okaże sie że ona jeździ na wózku inwalidzkim.<p class="post_modified">Zmieniony Wczoraj, 21:40:58 przez MCh)ZbeeR</p></div></div><div class="post" id="post_11"><div class="posthead"><div class="p2_data">Wczoraj, 21:43:34</div><div class="p2_nick"><span class="numerek_posta">[#11]</span>&nbsp;<a class="nick" href="/user/31840">Rodriguez</a></div></div><div class="post_body">dziewczynie/żonie kup roczny zapas płynu do mycia naczyń. ucieszy się jak nigdy.<br />\r\n<br />\r\nnie dziękuj.<p class="post_modified">Zmieniony Wczoraj, 21:43:50 przez Rodriguez</p></div></div><div class="post" id="post_12"><div class="posthead"><div class="p2_data">Wczoraj, 21:53:37</div><div class="p2_nick"><span class="numerek_posta">[#12]</span>&nbsp;<a class="nick" href="/user/29977">ktotoolo</a></div></div><div class="post_body">#10 o kurwa xd<p class="post_modified">Zmieniony Wczoraj, 21:53:54 przez ktotoolo</p></div></div><div class="post" id="post_13"><div class="posthead"><div class="p2_data">Wczoraj, 22:07:48</div><div class="p2_nick"><span class="numerek_posta">[#13]</span>&nbsp;<a class="nick" href="/user/9926">res)pEct</a></div></div><div class="post_body"><div class="cite" name="post_10">W 10 MCh)ZbeeR napisał: <a href="#" class="cite_link">[Pokaż]</a>\n                      <div class="cite_field"></div>\n                 </div> no tak, kobiety nie znaja swoich bliskich.</div></div><div class="post" id="post_14"><div class="posthead"><div class="p2_data">Wczoraj, 22:55:18</div><div class="p2_nick"><span class="numerek_posta">[#14]</span>&nbsp;<a class="nick" href="/user/19476">mACIoR</a></div></div><div class="post_body">pompkę do materacu</div></div><div class="post" id="post_15"><div class="posthead"><div class="p2_data">Wczoraj, 23:03:37</div><div class="p2_nick"><span class="numerek_posta">[#15]</span>&nbsp;<a class="nick" href="/user/28123">plepleple</a></div></div><div class="post_body">#7 pończochy stringi i pomarańcze. niech sobie dorobi do kompletu cyckonosz z połówek cytrusa.<p class="post_modified">Zmieniony Wczoraj, 23:04:44 przez plepleple</p></div></div><div class="post" id="post_16"><div class="posthead"><div class="p2_data">Wczoraj, 23:06:37</div><div class="p2_nick"><span class="numerek_posta">[#16]</span>&nbsp;<a class="nick" href="/user/21818">iS-Naab</a></div></div><div class="post_body">Coś do hygieny - np żel intymny na hemoroidy</div></div><div class="post" id="post_17"><div class="posthead"><div class="p2_data">Wczoraj, 23:08:24</div><div class="p2_nick"><span class="numerek_posta">[#17]</span>&nbsp;<a class="nick" href="/user/31840">Rodriguez</a></div></div><div class="post_body">albo używana szczoteczka do zębów?</div></div></div><ul class="forum_navi"><li><a href="/forum">Forum</a>&nbsp;&gt;&gt;&nbsp;</li><li><a href="/forum/4">OT</a>&nbsp;&gt;&gt;&nbsp;</li><li>Prezenty na święta - 2016</li></ul>\t</div>\n\t\n\t<div id="menu-wrapper">\n\t\n\t\t<div id="gora-menu">\n\t\t</div>\n\t\t\n\t\t<div id="menu-content">\n                    <div id="nowosci"></div>\n                    <div class="menu-pozycje">                            \n                        <a href="http://netwars.pl/forum/">Forum</a> \n                    </div>                                \n                    <div id=\'stream\'></div>\n                    <div class="menu-pozycje">                            \n                        <br />\n                    </div>\n\t\t</div>\n\t</div>\n\t\n</div>\t\n\n<div id="footer">\n    <b><a href=#top>Powrót na górę</a>  |  <a href="http://www.netwars.pl">Powrót do strony głównej forum</a></b><BR /><BR />\n        Użytkownicy online (53): <a href=\'/user/30480\'>4fiter</a>, <a href=\'/user/6189\'>Arosz</a>, <a href=\'/user/31908\'>ArTuDitu</a>, <a href=\'/user/12493\'>BazdA)PM</a>, <a href=\'/user/18578\'>BeMyValentine</a>, <a href=\'/user/31719\'>BoloMaster</a>, <a href=\'/user/29465\'>CaliSto</a>, <a href=\'/user/29475\'>DARKKKIS</a>, <a href=\'/user/29966\'>[DD]Ateriusz</a>, <a href=\'/user/6046\'>Dig</a>, <a href=\'/user/12530\'>DL)DarkLord</a>, <a href=\'/user/916\'>DooMo</a>, <a href=\'/user/30023\'>dspdsp</a>, <a href=\'/user/31377\'>freshu</a>, <a href=\'/user/30790\'>[GG]VIXA</a>, <a href=\'/user/9877\'>Gladius</a>, <a href=\'/user/31143\'>Grothen</a>, <a href=\'/user/11591\'>HaSskE[VBK]</a>, <a href=\'/user/32149\'>HiRosH</a>, <a href=\'/user/29371\'>IceColdKilla</a>, <a href=\'/user/31817\'>IIFaust</a>, <a href=\'/user/31254\'>Imagol</a>, <a href=\'/user/21998\'>Kami-</a>, <a href=\'/user/31824\'>kari88pl</a>, <a href=\'/user/31912\'>Kashim</a>, <a href=\'/user/28225\'>KEFiR</a>, <a href=\'/user/12929\'>Kisiel</a>, <a href=\'/user/9294\'>kogeT(GN)</a>, <a href=\'/user/7858\'>Krez</a>, <a href=\'/user/4102\'>LiM[CLK]</a>, <a href=\'/user/2321\'>LorD</a>, <a href=\'/user/32010\'>LordJim</a>, <a href=\'/user/31131\'>Maatek</a>, <a href=\'/user/28334\'>MadAngelo</a>, <a href=\'/user/26904\'>Misio_pysio</a>, <a href=\'/user/13767\'>NoX</a>, <a href=\'/user/1747\'>Piekny[DB]</a>, <a href=\'/user/28108\'>pre7ender</a>, <a href=\'/user/13142\'>Repomaniak</a>, <a href=\'/user/7201\'>Rocca</a>, <a href=\'/user/2997\'>RrA`Reksio</a>, <a href=\'/user/16440\'>ryszawa</a>, <a href=\'/user/398\'>Screwt[PiG]</a>, <a href=\'/user/1152\'>SeXyWombaT</a>, <a href=\'/user/28771\'>ShockeR_40</a>, <a href=\'/user/8207\'>USS.PhecY</a>, <a href=\'/user/29553\'>vinsky</a>, <a href=\'/user/29243\'>Vol</a>, <a href=\'/user/31744\'>WujekStefan</a>, <a href=\'/user/30148\'>yuC</a>, <a href=\'/user/31583\'>ZbikU</a>, <a href=\'/user/31870\'>ZiggyPG</a>, <a href=\'/user/7782\'>z.z.Werter</a></div>\n\n</body>\n</html>\n\n\t\n'

    def test__url_to_soup(self):
        self.fail()

    def test__topic_differences(self):
        self.fail()

    def test__live_user_differences(self):
        self.fail()

    def test__topic_soup_to_json(self):
        self.fail()

    def test_login(self):
        self.fail()

    def test_logout(self):
        self.fail()

    def test_topic_to_json(self):
        self.fail()

    def test__list_of_active_users(self):
        self.fail()

    def test__topics_and_post_number(self):
        self.fail()

    def test_home_page_status(self):
        self.fail()