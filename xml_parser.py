## XML Parser using  ElementTree-Api in Python
# TO run this code use : python3 filenname
import xml.etree.ElementTree as ET
import os
path = os.getcwd()
tree = ET.parse("C:\ProgramData\CAST\CAST\Extensions\com.castsoftware.bpel.0.1\\tests\BPEL_Sample\Oracle_Samples\Employee\Employee.wsdl")
root = tree.getroot()
print(root.tag,root.attrib)
dict={}
val = "0"          # index value
tmp= str(root.tag) # tmp making indexes unqiue
dict[tmp]="0"     # stroing all indexes in dicitonary
element_list=[]
#print (root.tag,root.attrib)
def parse_xml (root,val,tmp): #Recursive Function Print out elements and indexes
    if root is None :
        return
    val+= ".0"
    count = 0
    for child in root:
        if child.tag is not None:
            if count == 0:
                tmp+="_"
                tmp+=str(child.tag)
            else:
                ind = tmp.rfind('_')
                len_del = len(tmp)-ind-1
                tmp =tmp[:-len_del]
                tmp+=str(child.tag)
            tmp+=str(count)
            dict[tmp]=val
            print(child.tag)
            parse_xml(child,val,tmp)
            count=count+1
            ind=val.rfind('.')
            len_del = len(val)-ind-1
            val=val[:-len_del]
            val+=str(count)

        #if child.attrib is not None:
        #    print(child.attrib,end='')
        #if child.text is not None:
        #    print(child.text,end='')

parse_xml(root,val,tmp)
#print(dict)
