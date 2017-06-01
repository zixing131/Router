#encoding:utf-8
"""
@author:zixing 
@email:zixing@9smart.cn
@date:2017-06-02 02:46
"""
import urllib
import requests

class MercuryApi:
	def __init__(s,domainUrl,Pwd,showStatus=1):
		s.domainUrl = domainUrl #"http://192.168.0.1/"
		s.Pwd = Pwd
		s.TDDP()
		s.authInfo = []
		s.session = ""
		#s.UA = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
		#s.header = { "User-Agent" : s.UA,"Referer": "http://192.168.0.1" }
		#s.my_session = requests.Session()
		s.showStatus = showStatus
		
	def TDDP(s):
		#DM.js
		s.TDDP_INSTRUCT = 0
		s.TDDP_WRITE = 1
		s.TDDP_READ = 2
		s.TDDP_RESET = 5 #Reset the Router
		s.TDDP_REBOOT = 6
		s.TDDP_AUTH = 7
		s.TDDP_GETPEERMAC = 8
		s.TDDP_CHGPWD = 10
		s.TDDP_LOGOUT = 11
		
		#model.js
		s.DEVICE_DATA_ID = 0
		s.SYSTEM_DATA_ID = 1  
		s.SYSTEM_LOG_DATA_ID = 2
		s.EXCEPT_LOG_DATA_ID = 3
		s.LAN_DATA_ID = 4
		s.DHCPS_DATA_ID = 8
		
		s.WLAN_AP_LIST_DATA_ID = 38
		
	def post(s,url,data=""):
		return requests.post(url,str(data)).content

	def ConvertErrCode(s,errorCode):
		result = "Unknow Error"
		if(errorCode == 0):
			result = "Post Success"
		elif(errorCode == 7):
			result = "Password Error"
		elif(errorCode == 9):
			result = "Invalid Instruct"
		elif(errorCode == 114):
			result = "Same Password"
		return result

	def encodePara(s,a):
		return urllib.quote(a)
		
	def securityEncode(s,a,b,c):
		d, f, h, m = "", len(a), len(b), len(c)
		e = max(f,h)
		for g in range(0,e):
			l = k = 187
			if(g >= f):
				l = ord(b[g])
			else:
				if(g >= h):
					k = ord(a[g])
				else:
					k = ord(a[g])
					l = ord(b[g])
			d += c[ (k ^ l) % m ]
		return d
		
	def orgAuthPwd(s,Pwd = ""):
		return s.securityEncode(Pwd=="" and s.Pwd or Pwd, "RDpbLfCPsJZ7fiv", "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW")
		
	def getAuthInfo(s):
		result = s.post(s.getTDDPUrl(s.TDDP_READ)).split("\r\n")
		if(len(result) < 7): 
			return []
		s.authInfo = ["" for i in range(5)]
		for i in range(1,5):
			s.authInfo[i] = result[i].strip()
		
	def getSession(s):
		s.getAuthInfo()
		s.session = s.securityEncode(s.authInfo[3],s.orgAuthPwd(),s.authInfo[4])
		
	def printResult(s,loginResult,OperaName=""):
		if(s.showStatus == 0):
			return
		loginCode = int(loginResult.split("\r\n")[0])
		if (loginCode == 0):
			print("%s Success" % (OperaName))
		else:
			print("%s Failed , error code:%d , error msg:%s " %(OperaName,loginCode,MwApi.ConvertErrCode(loginCode)))

	def orgURL(s,a):
		s.getSession()
		return "%s%sid=%s"%(a,(a.find("?")>-1 and '&' or '?'),s.encodePara(s.session))
		if(a.find("?")>-1):
			return "%s&id=%s"%(a,s.encodePara(s.session))
		else:
			return "%s?id=%s"%(a,s.encodePara(s.session))
			
	def getTDDPUrl(s,TDDP,asyn=0):
		return "%s?code=%d&asyn=%d"%(s.domainUrl,TDDP,asyn)

	def auth(s): #auth user,just like login
		url = s.orgURL(s.getTDDPUrl(s.TDDP_AUTH))
		result = s.post(url)
		s.printResult(result,"Login")
		return result
	
	def read(s,a = ""):
		url = s.orgURL(s.getTDDPUrl(s.TDDP_READ))
		result = s.post(url, a=="" and s.SYSTEM_DATA_ID or a )
		s.printResult(result,"Read")
		return result
		
	def write(s,data = ""):
		url = s.orgURL(s.getTDDPUrl(s.TDDP_WRITE))
		result = s.post(url, data=="" and "" or data )
		s.printResult(result,"Write")
		return result
		
	def reboot(s):
		url = s.orgURL(s.getTDDPUrl(s.TDDP_REBOOT))
		result = s.post(url)
		s.printResult(result,"Reboot")
		return result 
	
	def changePwd(s,newPwd):
		url = s.getTDDPUrl(s.TDDP_CHGPWD)
		url += "&auth=" + s.encodePara(s.orgAuthPwd(s.Pwd))
		url = s.orgURL(url)
		result = s.post(url,s.orgAuthPwd(newPwd))
		s.printResult(result,"changePassWord")
		s.Pwd = newPwd
		return result
			
	def instr(s,instruct): #no use
		url = s.orgURL(s.getTDDPUrl(s.TDDP_INSTRUCT))
		result = s.post(url,instruct)
		s.printResult(result,"INSTRUCT")
		return result 
	
	def logout(s): #It seems useless but for safe exit in the browser
		url = s.orgURL(s.getTDDPUrl(s.TDDP_LOGOUT))
		result = s.post(url)
		s.printResult(result,"Logout")
		return result 
		
	def getPeerMac(s): #get your mac address
		url = s.orgURL(s.getTDDPUrl(s.TDDP_GETPEERMAC))
		result = s.post(url)
		s.printResult(result,"getPeerMac")
		return result 
		
	def reset(s): #Reset your Router!!!
		result = "Warning,this operation will reset your router!!!"
		print(result)
		return result
		
		url = s.orgURL(s.getTDDPUrl(s.TDDP_RESET))
		result = s.post(url)
		s.printResult(result,"reset")
		return result 

if(__name__ == "__main__"):
	MwApi = MercuryApi("http://192.168.0.1/","admin")
	MwApi.auth()
	#print(MwApi.getPeerMac())
	#print(MwApi.read(MwApi.DHCPS_DATA_ID)) 
	"""print(MwApi.write(
		'''id 8
		enable 1
		poolStart 192.168.0.60
		poolEnd 192.168.0.170
		leaseTime 120
		dns 0 180.76.76.76
		dns 1 223.6.6.6
		gateway 192.168.0.1
		hostName 
		'''))
	"""
	#print(MwApi.read(MwApi.SYSTEM_DATA_ID))
	#MwApi.changePwd("admin")
	#MwApi.logout()
	#MwApi.reboot()
