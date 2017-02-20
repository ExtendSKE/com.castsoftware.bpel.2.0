import xml.etree.ElementTree as ET
import re

def parse_xml(root, list1):
	for k in list(root.iter()) :
		data1 =re.sub('{.*?}', '',str(k.tag)) 
		if data1 == "invoke" :
			l = k
		if data1 == "javaCode" :
			print (l.attrib["name"])
			print (k.text)
			dict = { l.attrib["name"] : k.text}		
			list1.append(dict)
            
def getInvokeJavaCode(file) : 
	tree = ET.parse(file)
	root =tree.getroot()
	list1 = []
	parse_xml(root, list1)
	return list1