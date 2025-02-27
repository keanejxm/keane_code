#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  八戒网的接口.py
:time  2025/2/7 15:27
:desc  
"""
import json
import time
import requests


class BaJieWeb:
    def __init__(self):
        pass

    def _api_captcha_config(self):
        url = "https://account.zbj.com/api/captchaService/captchaConfig"
        headers = {
            "cookie": "_uq=83c578b8af7423a23fbab51ac50330bb; uniqid=d01maaw5nv232; _suq=709cf479-4e32-4cec-9514-bf8f4c6e4437; local_city_id=3374; local_city_path=beijing; local_city_name=%E5%8C%97%E4%BA%AC; Hm_lvt_a360b5a82a7c884376730fbdb8f73be2=1738725951; HMACCOUNT=C3AAB8DD0F63050E; jdymenuchannel=1; _un=15763940378; fromurl=4a63079ce307e07cf30a9cffab7753a96e7f99db7f6c17e966d9f993ab730c060332a51a968beccf025f1f798c6602c4e51b5f4383a7848c8351b15063e947485cd4382af7fa539512f8649065021847; wayType=603; unionJsonOcpc=eyJvdXRyZWZlcmVyIjoiaHR0cHM6Ly93d3cuYmFpZHUuY29tL290aGVyLnBocD9zYy5LNjAwMDBqMmd3UWowNi0iLCJwbWNvZGUiOiIxMzc1MzU4MDQiLCJ1dG1fc291cmNlIjoiYmRweiJ9; oldvid=97c9186b1feddcda66cc966026c7f247; vid=60f73dd1ab59c7db5fa52f68e9c87b6e; ssid=X6hjRro6UAISGEJm1jEYFnHR4iqBZNd1; osip=1738897847109; s_s_c=mf9g4pQe2XL9Jx9CXRxQeRNAuuZR46Ff%2B3H4jsDtifRMUolrZTQmCUsnpbdyDUz7%2FPjKoe9whI0v8hB5B0yXMA%3D%3D; Hm_lpvt_a360b5a82a7c884376730fbdb8f73be2=1738897862; nodejs-zbj-account-web=s%3ADBRIQivWc1EYQ3kEL8Aj6tc5tcADvyny.CudjprpJNbB6M%2BunsW341cIS0VCVMBtQspgwwVBXF0w",
            "origin": "https://account.zbj.com",
            "referer": "https://account.zbj.com/login?lgtype=1&waytype=603&fromurl=https%3A%2F%2Fwww.zbj.com%2Fsem%2Findex%3Fpmcode%3D137535804%26utm_source%3Dbdpz%26utm_medium%3DSEM",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        data = {
            "captchaType": "login",
            "clientType": "web",
            "scene": "pc_username_pwd"
        }
        res = requests.post(url, headers=headers, data=data)
        assert res.status_code == requests.codes.ok, "获取登录配置"
        res_json = json.loads(res.content)
        gt = res_json["data"]["gt"]
        challenge = res_json["data"]["challenge"]
        return gt, challenge

    def _api_slide(self,gt,challenge):
        url = "https://api.geetest.com/ajax.php"
        time_data = int(time.time()*1000)
        headers = {
            "Host":"api.geetest.com",
            "Referer":"https://account.zbj.com/login?lgtype=1&waytype=603&fromurl=https%3A%2F%2Fwww.zbj.com%2Fsem%2Findex%3Fpmcode%3D137535804%26utm_source%3Dbdpz%26utm_medium%3DSEM",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        data ={
            "gt":"11be06005fe5ab253c42091618255167",
            "challenge":"f5b35389d226242ab15fbd25e42bd07d",
            "lang":"zh-cn",
            "pt":"0",
            "client_type":"web",
            "w":"DGW1ZIUXYfazhhEIWQ(knRsxXiaOqKyKqciV2orGD8MfxAUxRIaK83g6H146m1k0u(dQjB5ywPyWzJJqTyw9LI9cLb7aTJchVDcq)(KyzRYnUHnQf2Kyy238s4rHTBHil0tshfOoRQU7zwATQMAumqwsWVEbPOSPipEOnyPPD2A7OGh)LrlqPwVsXd01Z4KgrbrniyMmeW4uq8TL5WLspeygORFcFuZlD11zybk8sJl9MAVaBcIyKozYaO(F0E8P0P1yytt9F5z0xUK76J(ZSw0u2ffuzBmDDsjfluspyGLDI1ecte5VTeoUgF9SdzsVYbBR)HgiQMPZAGd7qNAzrsBK1bAerSRM9Q3kbh93b4ildlD8GVRgu78S20bbNbM)48xMQrXW1GCbH9Fi2SooQCnf10mLiF89OKycE9kZbKXdiwQx2hc9Quw1kJNnQGBi1GybiXP1GuszbO25Y9w4r1xWBpRTVpgbai5K3pm57w7)99JYNNyrMKYYMUJ79j3hZmALPNGjjmxSjUQm4jV3PABgbe82a2O0odSISvbcl0rZmBRk4LSeWSD(Xjm1Fl4Qmf)VywGuMGgKobFrbYvi4uP3ZPXJ431wtseCy3j6q5EqdtXSlMdVwJY0(Nkjl(L9BYy2m0COLVa5ioayZd4r6OoXpVm7kiyYNRz7Ayf4wda0xAAXBZh2lLcBclYdoV7RjvbRKDCU2mJrDF08c)gI0lm1340sg9yBUXwYfa8f5dOcjgYLnlnqytTb8pWl60UwlHuBcM26IlGub5a8MWT0m64F7yknNJU0VOsN1SEAWa1xuRE()78PQeutKA9XAppAavpve4dm5iB8DbmNBfbo(F9DMiwfx37YiLcq4bP2DrwQyzJFjmxmPD97Rwzc8HulRzshiqvh9CxhdfdH32B1fzppKU58A4lkWZfNzN(MZzR7JJME53OIAcu4Rv0mCWBn3pzEQEmKNmwCgtKyoJfwMKihS7KsqVcds07e7sbQ605p(6aDzOqH7wrHhbVzpe6MdNTKOrCnf(h15V(nzC2(FwKGW0s8l1yVD(3EAevHFzotmfpjgDbsyUOm7PRBQEWdlE)QwBrKm76OxJ5ge9gMuM0orRr3i5hEdAs(Qu1C0sOUfnwbwWlZz6kIKZWC9(ONZReCMsccJyAVghUlHZvGQPJHo)CrhQmME0CR7KYMbjyzHZEhrCWkGM1jZOSR8znQErTprG0dqKbPrfdMtLQqF4OGrA9sndtWqwzoxXPmsiwu)2yrIArLWz)VfhCquS0up9k3pVONNCMIY7T91DBOWIP8WCKlHwKFAuyZrdCgLxyMhlRU8S9IPKXVoSdVDORT8BH(FZT6XcoPq6YtCZhX82gtshsLDncopD5UcYbTGW(4QGOb4lZAYDA3xVJhqVqVqBAcQUOEVRhgHId7sZv3o65HAe0CZzGG11InLxzdE3ayQNLLcuM7lvJCuUzEHzY2JEjRwrzaC5yiNYNlUAJR0PaXs6PyB6zB4ZDITQZEzODQc3nEiWjtpP8LJ1tA9lsP2T1(EJPLoADajRg1I1HJ(W(8KkTQeKxrPBjANQANtzc.",
            "callback": f"geetest_{time_data}"
        }
        res = requests.get(url,headers=headers,params=data)
        assert res.status_code == requests.codes.ok, "获取验证码图片接口错误"
        data = res.text.lstrip(f"geetest_{time_data}(").rstrip(")")
        data = json.loads(data)
        print(data)


    def _api_get_geetest(self, gt, challenge):
        time_data = int(time.time()*1000)
        url = "https://api.geetest.com/get.php"
        headers = {
            "Host": "api.geetest.com",
            "Referer": "https://account.zbj.com/login?lgtype=1&waytype=603&fromurl=https%3A%2F%2Fwww.zbj.com%2Fsem%2Findex%3Fpmcode%3D137535804%26utm_source%3Dbdpz%26utm_medium%3DSEM",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        data = {
            "is_next": "true",
            "type": "slide3",
            "gt": gt,
            "challenge": challenge,
            "lang": "zh-cn",
            "https": "true",
            "protocol": "https://",
            "offline": "false",
            "product": "embed",
            "api_server": "api.geetest.com",
            "timeout": "30000",
            "isPC": "true",
            "autoReset": "true",
            "width": "100%",
            "callback": f"geetest_{time_data}"
        }
        res = requests.get(url, headers=headers, params=data)
        assert res.status_code == requests.codes.ok, "获取验证码图片接口错误"
        data = res.text.lstrip(f"geetest_{time_data}(").rstrip(")")
        data = json.loads(data)
        print(data)

    def _api_demand(self):
        url = "https://jdyboss.zbj.com/api/DemandV3Service/getDemandHallListv3"
        headers = {
            "cookie": "_uq=83c578b8af7423a23fbab51ac50330bb; "
                      "uniqid=d01maaw5nv232; "
                      "_suq=709cf479-4e32-4cec-9514-bf8f4c6e4437; "
                      "unionJsonOcpc=eyJvdXRyZWZlcmVyIjoiaHR0cHM6Ly93d3cuYmFpZHUuY29tL290aGVyLnBocD9zYy5LZjAwMDBLUXYtcjRGZVEiLCJwbWNvZGUiOiIxMzc1MzU4MDgiLCJ1dG1fc291cmNlIjoiYmRweiJ9; "
                      "local_city_id=3374; "
                      "local_city_path=beijing; "
                      "local_city_name=%E5%8C%97%E4%BA%AC; "
                      "Hm_lvt_a360b5a82a7c884376730fbdb8f73be2=1738725951; "
                      "HMACCOUNT=C3AAB8DD0F63050E; "
                      "vidSended=1; "
                      "nsid=s%3AAeQeF1BHiDhvplPMky7VacXGcFrRoNMp.SP2QL2GTMLLIB6ZEMvF%2FiDL%2BoN5Z2KxBsH4qk%2Bf%2BXKU; "
                      "fromurl=75556ffa158ff22c20daf9f4d01536352d510c1a479e2584213771687957e84c; "
                      "s_s_c=mf9g4pQe2XL9Jx9CXRxQeRNAuuZR46Ff%2B3H4jsDtifRID5w32DRxlUBReG3unP%2BA6E44mIsr48aar1eN2Ggxsg%3D%3D; "
                      "nickname=%E9%A2%9C%E5%A4%A7%E5%93%A6; brandname=%E9%A2%9C%E5%A4%A7%E5%93%A6; "
                      "userid=33943900; "
                      "userkey=7otyUPV%2FWK%2B%2BscM3WN%2FRqYvQG7FC%2BuyyQn%2B3ZMoRn8U%2ByQWiYO6fFv6Rigu9ASyrFElwrTESGaB5I5RdPS%2BuMlzDVGs1d8OzZxl0ojeU%2FEu%2BlFy5f8nyc2nFfUCD%2Fr1bLzH%2BrCH%2F4Lkb62aUHwacR41UYbVAUXkZmE7D4OwUbmUI9Vpk1E0lKIA1byeAmsJAe56Vr5VO6WilpIuNY76l%2BkJPnF1%2BxlgqTQ8dl%2FRTJXNuBBRUI6Ief8WPkXSz8O%2B%2Frode665LTLmFAJPDO8JLeR4VKw%2FEK13LRJYM3OkQaOynzoHhRJaPlXiFBCWEMx2trtMr1NbNyvInow%3D%3D; "
                      "organizeId=1218984; "
                      "orgMaster=1; "
                      "shopName-33943900=%E9%A2%9C%E5%A4%A7%E5%93%A6; "
                      "jdymenuchannel=1; "
                      "jdy_manager_qr=1; "
                      "show-standard-service2025chujiehuodong33943900=1; "
                      "promotion33943900_ok=true; "
                      "Hm_lpvt_a360b5a82a7c884376730fbdb8f73be2=1738735187; "
                      "oldvid=60f73dd1ab59c7db5fa52f68e9c87b6e; "
                      "vid=97c9186b1feddcda66cc966026c7f247",
            "origin": "https://jdyboss.zbj.com",
            "priority": "u=1, i",
            "referer": "https://jdyboss.zbj.com/osg/open_hall?tab=0&supei=1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        data = {"pageNum": 1, "pageSize": 24, "source": 1, "sellerHallType": 4, "category1Id": [18216],
                "dispatchSearchType": [0]}
        res = requests.post(url, headers=headers, json=data)
        print(res.text)

    def start(self):
        gt, challenge = self._api_captcha_config()
        self._api_slide(gt,challenge)
        self._api_get_geetest(gt, challenge)


if __name__ == '__main__':
    obj = BaJieWeb()
    obj.start()
