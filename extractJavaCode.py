import xml.etree.ElementTree as ET
import re


def parse_xml(root,list1):
	if root is None:
		return
	for i in root:
		data =str(i.tag)
		data =re.sub('{.*?}', '',data)
		if data == "invoke":
			print("New")
			for k in list(i.iter()) :
				data1 =re.sub('{.*?}', '',str(k.tag)) 
				if data1 == "invoke" :
					l = k
				if data1 == "javaCode" :
					print (l.attrib["name"])
					print (k.text)
					dict = { l.attrib["name"] : k.text}		
					list1.append(dict)
		parse_xml(i,list1)
def getInvokeJavaCode(file) : 
	list1 = []
	tree = ET.parse(file)
	root =tree.getroot()
	parse_xml(root,list1)
	return list1

