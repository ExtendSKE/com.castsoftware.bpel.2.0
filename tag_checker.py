import xml.etree.ElementTree as ET
import re
#import cast.analysers.log as X
#import cast.analysers.log
def predefine_tags():
    #cast.analysers.log.debug(path+'')
    tags = ["receive","invoke","process"]
    return tags
def find_tag_properties(root,tag_name,list_data):
    if root is None:
        return list_data
    for i in root:
        index1 = str(i.tag)
        index1 =re.sub('{.*?}', '', index1)
        if tag_name == index1:
            data =str(i.attrib)
            data = re.sub('{','',data)
            data = re.sub('}','',data)
            if len(data)!=0:
                data = re.sub('[\s+]','',data)
                data= re.sub("'","",data)
                list_data.append(data)
        list_data = find_tag_properties(i,tag_name,list_data)
    return list_data
'''
def wsdl_data(root,operation_list_data):
    if root is None:
        return operation_list_data
    for i in root:
        data = str(i.tag)
        data =re.sub('{.*?}', '', data)
        if data == "operation":
            data =str(i.attrib)
            data = re.sub('{','',data)
            data = re.sub('}','',data)
            if len(data)!=0:
                data = re.sub('[\s+]','',data)
                data= re.sub("'","",data)
                operation_list_data.append(data)
        operation_list_data = wsdl_data(i,operation_list_data)  
    return operation_list_data
'''
def cast_parser_wsdl(filename):
    #cast.analysers.log.debug(path+'\n'+filename)
    #X.debug(filename)
    list_data = []
    operation_list_data = []
    tree = ET.parse(filename)
    root = tree.getroot()
    data =str(root.attrib)
    data = re.sub('{','',data)
    data = re.sub('}','',data)
    data = re.sub('[\s+]','',data)
    data= re.sub("'","",data)
    '''
    operation_list_data =wsdl_data(root,operation_list_data)
    for i in operation_list_data:
        print(i)
    '''
    list_data.append(root.tag)
    list_data.append(data)
    return list_data

def cast_parser_bpel(filename):
    tags = []
    bpel_tag_data = {}
    tags = predefine_tags()
    tree = ET.parse(filename)
    root = tree.getroot()
    for i in tags:
        list_data = []
        if i=="process":
            modified_data= str(root.attrib)
            modified_data = re.sub('{','',modified_data)
            modified_data = re.sub('}','',modified_data)
            if len(modified_data)!=0:
                modified_data = re.sub('[\s+]','',modified_data)
                modified_data= re.sub("'","",modified_data)
            list_data.append(modified_data)
            bpel_tag_data[i] = list_data
        else:
            bpel_tag_data[i]=find_tag_properties(root,i,list_data)
            #print(bpel_name_space_data[i])
    return tags,bpel_tag_data
if __name__ == "__main__":
    #tags = tag_finder()
    cast_parser_wsdl("C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.bpel.0.1\\tests\BPEL_Sample\Oracle_Samples\TravelProcess\Travel.wsdl")
