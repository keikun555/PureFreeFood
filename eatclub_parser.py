#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re


test_case_1 = """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--<![endif]-->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Eat Club</title>
<!--[if (gte mso 9)|(IE)]>
<style type="text/css">
    table {border-collapse:collapse !important !important;}
</style>
<![endif]-->

<style type="text/css">


	body { margin:0; padding:0; min-width:100%; background-color:#ffffff; }
	table { border-spacing:0; font-family:Tahoma, Verdana, Arial, sans-serif; color:#333333; }
	td { padding:0; }
	img { border:0; }
	.wrapper { width:100%; table-layout:fixed; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }
	.webkit { max-width:600px; }
	.outer { margin:0 auto; width:100%; max-width:600px; background-color:#f2f2f2; border-bottom:6px solid #ff5a00; }
	.outerwhite { width:100%; max-width:600px; background-color:#fff; }
	.outergrey { margin:30px auto 0; width:100%; max-width:600px; background-color:#e8e6e9; }
	.outerblue { margin:0 auto; width:100%; max-width:600px; background-color:#ff5a00; }
	.inner { padding:0; }
	.px404045 { padding:40px 40px 45px; }
	.px04045 { padding:0 40px 45px; }
	.px404030 { padding:40px 40px 30px; }
	.px40405 { padding:40px 40px 5px; }
	.px40400 { padding:40px 40px 0; }
	.px040 { padding:0 40px; }
	.px04010 { padding:0 40px 10px; }
	.px04040 { padding:0 40px 40px; }
	.px04065 { padding:0 40px 65px; }
	.px30025 { padding-top:30px; padding-bottom:25px; }
	.px60025 { padding-top:60px; padding-bottom:25px; }
	.px0025 { padding-bottom:25px; }
	.px0030 { padding-bottom:30px; }
	.px070 { padding:0 7px; }
	.px020 { padding:0 2px; }
	.block { display:block; }


	p,
	ul { margin:0; font-size:12px; line-height:18px; color:#707070; font-family:Tahoma, Verdana, Arial, sans-serif; }
	ul { padding-bottom:25px; padding-left:15px; }
	ul li { line-height:25px; }
	a { color:#6e6e6e; text-decoration:underline; }
	a.tel { text-decoration:none; }
	h1 { font-family:Arial Narrow, Arial, sans-serif; font-size:32px; line-height:40px; letter-spacing:0.75px; font-weight:600; color:#fff; text-transform:uppercase; }
	h2 { font-family:Arial Narrow, Arial, sans-serif; font-size:16px; letter-spacing:0.75px; color:#474747; text-transform:uppercase; font-weight:bold; }
	.left { text-align:left; }
	.center { text-align:center; }
	.outerblue p { color:#fff; }


	.btn { background-color:#ff5a00; width:297px !important; cursor:pointer; border-radius:4px; text-align:center; letter-spacing:0.5px; }
	.btn a { text-decoration:none; color:#fff; text-align:center; text-transform:uppercase; font-size:14px; line-height:56px; font-weight:800; }
	.outerblue .btn { background-color:#fff; }
	.outerblue .btn a { color:#ff5a00; }



	.full-width-image img { width:100%; max-width:600px; height:auto; }


	.one-column p { font-size:12px; padding-bottom:25px; }


	.two-column { font-size:0; }
	.two-column .column { width:100%; max-width:310px; display:inline-block; vertical-align:top; }
	.two-column .contents { font-size:14px; text-align:left; }
	.two-column img { width:100%; max-width:124px; height:auto; }
	.two-column .text { padding:0 0 40px; }


	.three-column { font-size:0; }
	.three-column .column { width:100%; max-width:173px; display:inline-block; vertical-align:top; }
	.three-column .contents { font-size:14px; text-align:center; }
	.three-column img { width:100%; max-width:124px; height:auto; }
	.three-column .text { padding:20px 15px 40px; }


	.footer p,
	.footer p a { color:#9f9f9f; font-size:10px; text-align:center; }


@media screen and (max-width:450px) {

	.three-column .column { max-width:90% !important; }
    .btn { width:100% !important; background-image:none !important; }

}
</style>

<style>
  @media only screen and (max-width: 600px) {
    /* mobile css */
    .container {
      width: 100% !important;
      background-color: #fff !important;
    }
    .title-cont {
      padding: 8px 5% 18px 5% !important;
    }
    .title {
      font-size: 0.9em !important;
      line-height: 160% !important;
    }
    .subtitle {
      font-size: 12px;
    }
    .button {
      width: 100% !important;
      background-color: #FF5a00 !important;
      border-radius: 5px !important;
    }
    .button-inner {
      color: #FFFFFF !important;
      font-family: 'Roboto', Helvetica, Arial, sans-serif !important;
      font-size: 16px !important;
      font-weight: semibold !important;
      letter-spacing: 0.5px !important;
      height: 50px !important;
      text-align: center !important;
    }
    .button-link {
      color: #FFFFFF !important;
      text-decoration: none !important;
    }
    .button-cont {
      width: 100% !important;
      padding: 20px 5% !important;
    }
    .bag-id {
      font-size: 20px;
      font-weight: 600;
    }
    .bag-cont {
      padding-top: 14px;
    }
    .bag-item {
      font-size: 14px;
    }
  }
</style>


</head>
<body style="margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;min-width:100%;background-color:#ffffff;" >
    <div align="center" class="wrapper" style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;" >
        <div class="webkit" style="max-width:600px;" >

          <!--[if (gte mso 9)|(IE)]>
			<table width="600" align="center" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
			<tr>
			<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
			<![endif]-->
			<table class="px30025 outerwhite center" align="center" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;width:100%;max-width:600px;background-color:#fff;padding-top:30px;padding-bottom:25px;text-align:center;" >
				<tr>
					<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
            <a href="https://www.eatclub.com" style="color:#ff5a00;text-decoration:none;" >
              <img src="https://myeatclub.a.ssl.fastly.net/static/img/ec_logo_white_letters.png" width="100px" alt="EAT Club" style="border-width:0;" />
            </a>
					</td>
				</tr>
			</table>
			<!--[if (gte mso 9)|(IE)]>
			</td>
			</tr>
			</table>
			<![endif]-->

<!-- Content -->

      
<div style="border-bottom: 4px solid #FF5a00" >

<table class="container" style="width: 600px;background-color: #fff !important">
  <tr>
    <td align="center" class="title-cont" style="padding: 0 30px;padding-bottom: 20px;">
      <span class="title" style="font-size: 28px;line-height: 42px">
        Lunch is here!
      </span>
    </td>
  </tr>
</table>
<table class="container" style="width: 600px;background-color: #fff !important">
  <tr>
    <td align="center" class="subtitle-cont">
      <span class="subtitle">
        Your order is ready
        
          at 650 Castro Street 3rd Floor
        
      </span>
    </td>
  </tr>
</table>




<table class="container" style="width: 600px;background-color: #fff !important">
  <tr>
    <td align="center">
      <span class="rack-loc" style="font-size: 86px;font-weight: 600; color: #9B9B9B">
        D3
      </span>
    </td>
  </tr>
</table>
<table class="container" style="width: 600px;background-color: #fff !important">
  <tr>
    <td align="center">
      <strong>
        Beef Bibimcup
      </strong>
      from Bibimbowl
    </td>
  </tr>
</table>
<!-- Review your dish button -->
<table class="container" style="width: 600px;background-color: #fff !important; padding-bottom: 50px">
  <tr>
    <td align="center" class="button-cont" style="padding: 20px 0 10px 0">
      <table border="0" cellpadding="0" cellspacing="0" class="button" style="width: 270px;background-color: #FF5a00;border-radius: 5px">
        <tr>
          <td align="center" valign="middle" class="button-inner" style="color: #FFF;font-family:'Roboto',Helvetica,Arial, sans-serif;font-size: 15px !important;font-weight: 300;letter-spacing: 0.5px;height: 50px">
            <a href="https://www.eatclub.com/orders/past" target="_blank" class="button-link" style="display: block;color: #FFF;text-decoration: none;width: 100%;min-width: 200px;line-height: 50px;height: 100%">
              REVIEW YOUR DISH
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
<!-- end -->







</div>




<!-- footer -->
			<!--[if (gte mso 9)|(IE)]>
			<table width="600" align="center" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
			<tr>
			<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
			<![endif]-->
			<table class="outerwhite center" align="center" width="100%" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;width:100%;max-width:600px;background-color:#fff;text-align:center;" >
				<tr>
					<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
            <table align="center" width="100%" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
              <tr>
                <td >
									<p class="center" style="margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;font-size:12px;line-height:18px;color:#707070;font-family:Tahoma, Verdana, Arial, sans-serif;padding-top:60px;padding-bottom:15px;text-align:center;" >
                    <a href="https://itunes.apple.com/us/app/eat-club/id555359589?mt=8&utm_campaign=website&utm_source=sendgrid.com&utm_medium=email"><img src="https://myeatclub.a.ssl.fastly.net/im/1451/" alt="appstore" height="50" width="142" border="0" style="padding-right:14px;"></a>
                    <a href="https://play.google.com/store/apps/details?id=com.myeatclub&hl=en"><img src="https://myeatclub.a.ssl.fastly.net/im/5369/" alt="googleplay" height="50" width="150" border="0"></a>
                  </p>
                </td>
              </tr>
            </table>
						<table align="center" width="100%" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
							<tr>
								<td>
									<p class="px0025 center" style="margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;font-size:12px;line-height:18px;color:#707070;font-family:Tahoma, Verdana, Arial, sans-serif;padding-bottom:25px;text-align:center;" >
                    <a href="https://www.instagram.com/eat_club/" title="Instagram" style="color:#6e6e6e;text-decoration:none;" >
                      <img src="https://myeatclub.a.ssl.fastly.net/im/8913/"  class="px070" alt="Instagram" style="display:inline-block;border-width:0;padding-top:0;padding-bottom:0;padding-right:7px;padding-left:7px;" height="30" width="30"/>
                    </a>&nbsp;
                    <a href="https://www.facebook.com/eatclub" title="Facebook" style="color:#6e6e6e;text-decoration:none;" >
                      <img src="https://myeatclub.a.ssl.fastly.net/im/8911/"  class="px070" alt="Facebook" style="display:inline-block;border-width:0;padding-top:0;padding-bottom:0;padding-right:7px;padding-left:7px;" height="30" width="30" />
                    </a>&nbsp;
                    <a href="https://twitter.com/eatclub" title="Twitter" style="color:#6e6e6e;text-decoration:none;" >
                      <img src="https://myeatclub.a.ssl.fastly.net/im/8915/"  class="px070" alt="Twitter" style="display:inline-block;border-width:0;padding-top:0;padding-bottom:0;padding-right:7px;padding-left:7px;" height="30" width="30"/>
                    </a>
                  </p>
								</td>
							</tr>
						</table>
						<table align="center" class="footer" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
							<tr>
								<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
									<p class="px0025 center" style="margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;line-height:18px;font-family:Tahoma, Verdana, Arial, sans-serif;padding-bottom:25px;color:#9f9f9f;font-size:10px;text-align:center;" >Copyright &copy; 2008-2019 | All rights reserved.
                    <br/>EAT Club, Inc., 1400A Seaport Blvd., Suite #400, Redwood City, CA 94063
                  </p>
								</td>
							</tr>
						</table>
						<table align="center" class="footer" style="border-spacing:0;font-family:Tahoma, Verdana, Arial, sans-serif;color:#333333;" >
							<tr>
								<td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;" >
									<p class="px0030 center" style="margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;line-height:18px;font-family:Tahoma, Verdana, Arial, sans-serif;padding-bottom:30px;color:#9f9f9f;font-size:10px;text-align:center;" >
                    You received this email because you are a member of
                    <a href="https://www.eatclub.com" style="text-decoration:underline;color:#9f9f9f;font-size:10px;text-align:center;" >EAT Club</a>.
                    
                    <br/>
                    <a href="https://www.eatclub.com/terms" style="text-decoration:underline;color:#9f9f9f;font-size:10px;text-align:center;" >Terms and Conditions</a> |
                    <a href="https://www.eatclub.com/contact" style="text-decoration:underline;color:#9f9f9f;font-size:10px;text-align:center;" >Contact Us</a>
                  </p>
								</td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
			<!--[if (gte mso 9)|(IE)]>
			</td>
			</tr>
			</table>
			<![endif]-->

        </div>
    </div>

<img src="http://em.eatclub.com/wf/open?upn=V2cY2Xoc6JAfTJ-2FYdZYnsWbKjcyUWQdvRvyEvyyusIvjDlLCK3Hq-2FL53v10W-2F5Vxif7leQvEECLTEW6xPXKMB7Y0reizrnl54bWaR2z8wFXTD-2FsFK2NnehJ-2B6QX3H4NrWtX21-2FimS4YhQlv7zRt-2FIlhUAEpop0WiWOFxwzGLRNdph-2FOHOIswcpGnxbnMBmao3VsUBJccexOug4O4UZW-2B17WDt4CC-2BEjTBnmeU4LcGp7n2OjQ6CYTvp5jy-2BfFsFnw-2BhWtMB0vcRnjHS37IUt1trq4nGp0YZRY0UCk1AXT7c4-3D" alt="" width="1" height="1" border="0" style="height:1px !important;width:1px !important;border-width:0 !important;margin-top:0 !important;margin-bottom:0 !important;margin-right:0 !important;margin-left:0 !important;padding-top:0 !important;padding-bottom:0 !important;padding-right:0 !important;padding-left:0 !important;"/>
</body>
</html>
"""

test_case_2 = '''
<table class=3D"container" style=3D"width: 600px;background-color: #fff !imp=
ortant">
  <tbody><tr>
    <td align=3D"center" class=3D"title-cont" style=3D"padding: 0 30px;paddi=
ng-bottom: 20px;">
      <span class=3D"title" style=3D"font-size: 28px;line-height: 42px">
        Lunch is here!
      </span>
    </td>
  </tr>
</tbody></table>
<table class=3D"container" style=3D"width: 600px;background-color: #fff !imp=
ortant">
  <tbody><tr>
    <td align=3D"center" class=3D"subtitle-cont">
      <span class=3D"subtitle">
        Your order is ready
       =20
          at 650 Castro Street 3rd Floor
       =20
      </span>
    </td>
  </tr>
</tbody></table>




<table class=3D"container" style=3D"width: 600px;background-color: #fff !imp=
ortant">
  <tbody><tr>
    <td align=3D"center">
      <span class=3D"rack-loc" style=3D"font-size: 86px;font-weight: 600; co=
lor: #594A41">
        G3
      </span>
    </td>
  </tr>
</tbody></table>
<table class=3D"container" style=3D"width: 600px;background-color: #fff !imp=
ortant">
  <tbody><tr>
    <td align=3D"center">
      <strong>
        Vegetable Coconut Curry
      </strong>
      from The Tandoori Door
    </td>
  </tr>
</tbody></table>
<!-- Review your dish button -->
<table class=3D"container" style=3D"width: 600px;background-color: #fff !imp=
ortant; padding-bottom: 50px">
  <tbody><tr>
    <td align=3D"center" class=3D"button-cont" style=3D"padding: 20px 0 10px=
 0">
      <table border=3D"0" cellpadding=3D"0" cellspacing=3D"0" class=3D"butto=
n" style=3D"width: 270px;background-color: #FF5a00;border-radius: 5px">
        <tbody><tr>
          <td align=3D"center" valign=3D"middle" class=3D"button-inner" styl=
e=3D"color: #FFF;font-family:'Roboto',Helvetica,Arial, sans-serif;font-size:=
 15px !important;font-weight: 300;letter-spacing: 0.5px;height: 50px">
            <a href=3D"https://www.eatclub.com/orders/past" target=3D"_blank=
" class=3D"button-link" style=3D"display: block;color: #FFF;text-decoration:=
 none;width: 100%;min-width: 200px;line-height: 50px;height: 100%">
              REVIEW YOUR DISH
            </a>
          </td>
        </tr>
      </tbody></table>
    </td>
  </tr>
</tbody></table>
'''


def grab_info(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    infos = {}
    for table in soup.find_all('table'):
        if "Your order is ready" in str(table.text):
            infos["address"] = re.findall("at\\s+(.*)", table.text)[0]
        elif "rack-loc" in str(table):
            infos["location"] = table.find('span').text.strip()
        elif table.find('strong'):
            infos["food"] = table.find('strong').text.strip()
            infos["restaurant"] = re.findall("from\\s+(.*)", table.text)[0]
        else:
            pass
    return infos


if __name__ == "__main__":
    print(grab_info(test_case_1))
    print(grab_info(test_case_2))
