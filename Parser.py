import xml.etree.ElementTree as ET
import re
import hashlib
class CastOperation():
    
    def __init__(self):
        self.tag_names = []
        self.bpel_file_data = {}
        self.wsdl_file_data = {}
        self.check_sum_with_commented_lines = ""
        self.check_sum_without_commented_lines = ""
        
    def defineTagNames(self):
        self.tag_names = ["receive","invoke","process","partnerLink","onMessage"]
        
    def parseNsmap(self,filename,NS_MAP):
        def parseNsXml(root,tag):
            for child in list(root.iter()):
                if tag in re.sub('{.*?}','',str(child.tag)) :
                    return(re.sub('({)|(})|(\')|(\s+)' ,'',str(child.attrib)).split(','))
                
        self.events =["start","start-ns","end-ns"]
        self.root_ns = None
        self.ns_map = []
        for event,elem in ET.iterparse(filename,self.events):
            if "start-ns" in  event:
                self.ns_map.append(elem)
            elif "end-ns" in event:
                self.ns_map.pop()
            elif "start" in event:
                if self.root_ns is None:
                    self.root_ns = elem
                elem.set(NS_MAP,dict(self.ns_map))
        if filename.endswith('.wsdl'):
            return parseNsXml(ET.ElementTree(self.root_ns),"definitions")
        else:
            return parseNsXml(ET.ElementTree(self.root_ns),"process")
        
    def getTagAttrib(self,root,tag):
        def getNamespace(ele):
            namespace = re.match('\{.*\}',ele.tag)
            return namespace.group(0) if namespace else ''
        
        self.namespace = getNamespace(root)
        self.tag_attrib = []
        match = './/%s'+tag
        for child in root.findall(match % self.namespace):
            self.tag_attrib.append(re.sub('({)|(})|(\')|(\s+)' ,'',str(child.attrib)).split(','))
        return self.tag_attrib
    
    def castParserWsdl(self,filename):
        self.wsdl_file_data["definitions"] = self.parseNsmap(filename,"xmlns:map")
        return self.wsdl_file_data
    
    def castParserBpel(self,filename):
        self.defineTagNames()
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        for child_tag in self.tag_names:
            if "process" in child_tag:
                self.bpel_file_data[child_tag]  = self.parseNsmap(filename,"xmlns:map")
            else:
                self.bpel_file_data[child_tag] = self.getTagAttrib(self.root,child_tag)
        return self.bpel_file_data
    
    def getInvokeJavaCode(self, filename) :
        tree = ET.parse(filename)
        root =tree.getroot()
        invokeJavaCodeList = []
        for child in list(root.iter()) :
            tag = re.sub('{.*?}', '',str(child.tag))
            if tag == "invoke":
                invokeTag = child
            if tag == "javaCode" :
                dict = { invokeTag.attrib["name"] : child.text}
                invokeJavaCodeList.append(dict)
        return invokeJavaCodeList
    
    def fileLoc(self,filename):
        md5_data_with_commented_lines = hashlib.md5()
        md5_data_without_commented_lines = hashlib.md5()
        line_of_code =0
        line_of_comments = 0
        no_of_blank_lines = 0
        flag = 0
        with open(filename,'r') as source_file:
            for line  in source_file:
                if flag == 1:
                    md5_data_with_commented_lines.update(line.encode('utf-8'))
                    if line.find('-->')==-1:
                        line_of_comments = line_of_comments + 1
                    else:
                        line_of_comments = line_of_comments + 1
                        flag = 0
                else:
                    if len(line) == 1:
                        no_of_blank_lines =no_of_blank_lines + 1
                    elif line.find('<!--')!=-1:
                        md5_data_with_commented_lines.update(line.encode('utf-8'))
                        line_of_comments = line_of_comments + 1
                        flag = 1
                        if line.find('-->')!=-1 and line.find('-->') > line.find('<!--'):
                            flag =0
                    else:
                        md5_data_with_commented_lines.update(line.encode('utf-8'))
                        md5_data_without_commented_lines.update(line.encode('utf-8'))
                        line_of_code = line_of_code +1
        self.check_sum_with_commented_lines = str(md5_data_with_commented_lines.hexdigest())
        self.check_sum_without_commented_lines = str(md5_data_without_commented_lines.hexdigest())  
        return [line_of_comments,line_of_code]
    
    def fileChecksum(self,filename):
        return [self.check_sum_with_commented_lines,self.check_sum_without_commented_lines]
    pass


if __name__ == "__main__":
    '''
    operation = CastOperation()
    print(operation.getInvokeJavaCode("Travel.bpel"))
    '''
    pass
