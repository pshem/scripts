#!/usr/bin/env python

import string

ciphertext = []

ciphertext.append("BoPjcSb KPW OoCb QP E GlghZnqYguHRr UEZiwm KX 1505. lLv TOkhoV ucS CwTViiyQGXdR, d dOkrsGgcN bt qVRsnWC, YaQhf gZnmI rjE 15gv RIatFfa YJ D kcije sR rqWa ocH N sFPWbFDq SgkaDI gp cNDgMNnz, WP K RHlUVSoBLmqD PoaPRd QSPSPL ESZRss (fcnLNGd'W OaCbU), SRFoiRZnq Xfg hbzn xeiyWVi GKddSc. TrI ajAczPMa wlg TOQXqSfRtoH ccCU MTEe wthJ K VHjiZRr CEjcRl, ocH N sFdRVc Ri TWieGSmf. tUs UEZiwm EYEW rT OimC aYu 'oa o QPhe qWGVH WkfSV roH-rqNTITH TowR NSSQ kSOUs sR qkDR JXIj'.")
ciphertext.append("FlaKVc WuSS ff QMmxAa PPXgiDhC lIOoOgf")
ciphertext.append("BoPjcSb FTGRiGSF K HHjfSV ix GgxIY zPa Nt EVG ERLySfjiDc mh pNrjE Vn 1538.")
ciphertext.append("eVG pVHqQV RuDLmt, bYoXWR dp JKQIQhfS, iezSpvEQ HWEg hp kCc WHujWeg kW Y uEPFTXNrJ WP dLH viWke yJ AcRQwcEY RzRQVJR SWc Ui MEprI NBS GeeoWVOH Kla kZtr Xfg IaJTRgizb QP XKh fSTizVmeAY HPFYe, ycY MEOoSR kho hcnLN ddVga EODVI. krkSmeB, fcnLNGd RRvpf OORWlcbVd MEpfIaoa tVo tb JSW ErcYj axH czPYoXRRd EVCd MQ 1550 kS kRs sR rjE fsgZVcp cH mEUgWbRl NYpcNgw XR paxSTSRR dbR Yan Xm wSR GTGeeE QQbVHvdcedoRag Ia HWI ftlhG KJIdWfj wrMjg HVG bEftpf YKW Lq Fcde pSp c CbBRPNvp. JGbWHg Wb ieCIYtCU, oQPR iy aCdLHpOhZcC, fcnLNGd HRawh YSXK vSQieD apkTVBV Eg a EWOO aKhb hYiC Epv EaxdcRd rfGKX DgaWiaDMmp Ia oaP ghp wVKPLdb QfuBXq, oAVBac Vn EVG BSPdb qlrsE. Gp TUwh KbloSP ZIUlcR ff DLc jIfHdVl oq QTiTWrUfRprc, fg WNG YYft zbG YJ Pdbm jemVcvAewTW jhz, cWd SI lbhVlvIavUNz eEfstcP YV Irf fVav RceEfGXXl, eIdGbMPhbhVd GMrj NRK hcftpaU NYUlbU khoMp fAVzn EPttjKdMHv. vWj csTfgR ZogORd lb GZSFk ObU wkW aqNfwSIeeo iPLVHdYOSlo Jmt FbIg GRnEiTSIV. Dg O jtEHcpT bt RMchpfU, RI PhbhZoxIb cMbBV LVs pbVRYVlOgks wElA EZwcIat rSPdPHpSb Rnn 'KpgAg DgMacpg'. kX 1552, LH pSh ToERr RAbzd eiorOFbS, Fribk GsElhRNBRIfcz uCWFDuO, Oed DLc tEaClRRd HfKdIU JWfflkQm TUfqTPYi, lZUY EQ hldVrD Ml uEPFTX jrthKXK, Zkc iigoH fkM gC gIcrtbV K VHfWdiomEj vAOzT XUaE VG gEV fWfTuvErkNT wc PboDS-NOEI icfd, ix TpkNg ocH ZayiUMVLsh. HYe DEZnE joh Xb bp RWVc FradceDIb yIgv iLR iygVbYFwWces. MSnkEf CU XUeDS VKFOhg SoiCX gp CbBiIZpzfCbc SuWjRto GmnLRqiMbnD WP pPRuSbTe kRb TOZs.")
ciphertext.append("- LMXiASFSE")
ciphertext.append( "fRBHvXdmQ{qThoWYggGW4aWVJnR24d1T1zwGlpBgIbQ3Okuna2,MEUhSfj@cyRrgXgwh.Gbm}(XOaLI Lwg QRso WcpSVHXZR?)")



oldCiphertext = "Olujl! ovtl, FvB pksl jylhABylz nlA FvB ovtl:"
oldCiphertext += " Pz Aopz h ovspkhF? DohA! ruvD FvB uvA,"
oldCiphertext += " Ilpun tljohupjhs, FvB vBnoA uvA Dhsr"
oldCiphertext += " bwvu h shivBypun khF DpAovBA Aol zpnu"
oldCiphertext += " Vm FvBy wyvmlzzpvu? Zwlhr, DohA Ayhkl hyA AovB?"

oldCiphertext += "- Zohrlzwlhy"
oldCiphertext += "JVUaLeaPZ{tsyBjupBj9ksGos9ky4j8xpmo0G3uq0CBxAFD0zv,AhsluA@jAE.pz}"


lowerUpper = string.ascii_lowercase + string.ascii_uppercase #+ string.digits

def decode(encrypted, rot, rotatingSurface):
	result = ""
	for i in range(len(encrypted)):
		if encrypted[i] in rotatingSurface:
			for j in range(len(rotatingSurface)):
				if encrypted[i] == rotatingSurface[j]:
					result += rotatingSurface[(j + rot) % len(rotatingSurface)]
					#result = rotatingSurface[len(rotatingSurface) - i]
		else:
			#don't change
			result += encrypted[i]
	return result


#def test():
	if decode(oldCiphertext, 19, lowerUpper) == "Hence! home, YoU idle creaTUres geT YoU home:":
		print("Decoding works")
		return true
	else:
		raise ValueError('Something is wrong with decode')
		return false

"""
if test():
"""

for b in range(len(lowerUpper)):
	print(b, " ", decode(oldCiphertext, b, lowerUpper))
"""
	print()
else:
	#print("Your code broke again")
"""
