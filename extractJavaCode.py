import xml.etree.ElementTree as ET
import re

def parse_xml(root, invokeJavaCodeList):
	for k in list(root.iter()) :
		data1 =re.sub('{.*?}', '',str(k.tag)) 
		if data1 == "invoke" :
			invokeTag = k
		if data1 == "javaCode" :
			dict = { invokeTag.attrib["name"] : k.text}		
			invokeJavaCodeList.append(dict)
            
def getInvokeJavaCode(file) : 
	tree = ET.parse(file)
	root =tree.getroot()
	invokeJavaCodeList = []
	parse_xml(root, invokeJavaCodeList)
	return invokeJavaCodeList