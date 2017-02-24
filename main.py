import cast.analysers.ua
import cast.analysers.log as CAST
import re
from cast.analysers import CustomObject,Bookmark,create_link
from Parser import CastOperation
wsdl_file_data = {}
bpel_process_data = {}
bpel_invoke_data = {}
bpel_receive_data = {}
wsdl_obj_reference = {}
class BpelExtension(cast.analysers.ua.Extension):
    def __init__(self):
        self.filename = ""
        self.name = ""
        self.invokeList = []
        self.file_loc_data = []
        self.file_checksum_data = []  
        pass
    def start_analysis(self):
        self.intermediate_file = self.get_intermediate_file("bpel.txt")
        pass
    def start_file(self,file):
        self.filename = file.get_path()
        parser = CastOperation()
        if self.filename.endswith(".wsdl"):
            try :
                    index = self.filename.rfind('\\')
                    self.name = self.filename[index+1:]
            except:
                    index =-1
            wsdl_process = CustomObject()
            self.saveObject(wsdl_process,self.name,self.filename,"WSDL_Process",file,self.filename+"WSDL_Process")
            wsdl_process.save()
            wsdl_process.save_position(Bookmark(file,1,1,-1,-1))
            wsdl_file_data[wsdl_process] = parser.castParserWsdl(self.filename)   
            self.file_loc_data = parser.fileLoc(self.filename)
            self.file_checksum_data = parser.fileChecksum(self.filename)
            wsdl_process.save_property("File_Data.line_Code",self.file_loc_data[0])
            wsdl_process.save_property("File_Data.commented_Line_Code",self.file_loc_data[1])
            wsdl_process.save_property("File_Data.check_sum_with_commented_lines",self.file_checksum_data[0])
            wsdl_process.save_property("File_Data.check_sum_without_commented_lines",self.file_checksum_data[1])
            #CAST.debug(self.name)
        else:
            self.invokeList = parser.getInvokeJavaCode(self.filename)
            for child in self.invokeList:
                self.intermediate_file.write(str(child)+'\n')
            bpel_data = parser.castParserBpel(self.filename)
            for child in bpel_data:
                #attrib_data = re.sub('(\[)|(\])|(\')','',str(bpel_file_data[child]))
                if "process" in child:
                    for subchild in bpel_data[child]:
                        if "name" in subchild:
                            self.name = subchild[subchild.find(':')+1:]
                            break
            bpel_process =CustomObject()
            self.saveObject(bpel_process,self.name,self.filename,"BPEL_Process",file,self.filename+"BPEL_Process")
            bpel_process.save()
            bpel_process.save_position(Bookmark(file,1,1,-1,-1))
            bpel_process_data[bpel_process] = bpel_data["process"]
            bpel_invoke_data[bpel_process] = bpel_data["invoke"]
            bpel_receive_data[bpel_process] = bpel_data["receive"]
            self.file_loc_data = parser.fileLoc(self.filename)
            self.file_checksum_data = parser.fileChecksum(self.filename)
            bpel_process.save_property("File_Data.line_Code",self.file_loc_data[0])
            bpel_process.save_property("File_Data.commented_Line_Code",self.file_loc_data[1])
            bpel_process.save_property("File_Data.check_sum_with_commented_lines",self.file_checksum_data[0])
            bpel_process.save_property("File_Data.check_sum_without_commented_lines",self.file_checksum_data[1])
            #CAST.debug(str(bpel_file_data[child]))
            pass
    def saveObject(self,obj_reference,name,fullname,type,parent,guid): 
        obj_reference.set_name(name)
        obj_reference.set_fullname(fullname)
        obj_reference.set_type(type)
        obj_reference.set_parent(parent)
        obj_reference.set_guid(guid) 
        pass
    def end_file(self,file):
        pass
    def end_analysis(self):
        for child in bpel_process_data:
            bpel_target_name = ""
            bpel_name  = ""
            for ele in bpel_process_data[child]:
                if "targetNamespace:" in  ele:
                    bpel_target_name = ele[ele.find(':')+1:]
                elif "name:" in ele:
                    bpel_name = ele[ele.find(':')+1:]
                
            for ele in wsdl_file_data:
                wsdl_target_name = ""
                wsdl_name = ""
                for subele in wsdl_file_data[ele]["definitions"]:
                    if "targetNamespace:" in subele:
                        wsdl_target_name = subele[subele.find(':')+1:]
                    elif "name:" in subele:
                        wsdl_name = subele[subele.find(':')+1:]
                #CAST.debug(wsdl_name)
                if wsdl_target_name == bpel_target_name:
                    create_link('callLink',ele,child,Bookmark(child.parent,1,1,-1,-1))
                    wsdl_obj_reference[child] = ele
                elif wsdl_name == bpel_name and len(wsdl_name)!=0 and len(bpel_name)!=0:
                    #CAST.debug(bpel_name+wsdl_name)
                    create_link('callLink',ele,child,Bookmark(child.parent,1,1,-1,-1))
                    wsdl_obj_reference[child] = ele
        invoke_count = 0
        operation_count =0 
        for child in bpel_invoke_data:
            for ele in bpel_invoke_data[child]:
                port_type = ""
                operation_type = ""
                invoke_name = "null"
                patnerlink_name = ""
                ele_data = str(ele)
                ele_data = re.sub('(\[)|(\])|(\')','',ele_data)
                bpel_invoke_list = []
                bpel_invoke_list = ele_data.split(',')
                for subele in bpel_invoke_list:
                    if 'portType:' in subele:
                        port_type = subele[subele.find(':')+1:]
                    elif 'operation:' in subele:
                        operation_type = subele[subele.find(':')+1:]
                    elif 'name:' in  subele:
                        invoke_name = subele[subele.find(':')+1:]
                    elif 'partnerLink' in subele:
                        patnerlink_name = subele[subele.find(':')+1:]
                filename = child.parent.get_path()
                invoke_fullname = ''
                if invoke_name == "null" :
                    invoke_name = patnerlink_name
                    invoke_fullname = filename+'--null'
                else:
                    invoke_fullname = filename+'--'+invoke_name
                    
                bpel_invoke = CustomObject()
                invoke_count =invoke_count+1
                self.saveObject(bpel_invoke,invoke_name,invoke_fullname,"BPEL_Invoke",child.parent,filename+"BPEL_Invoke"+str(invoke_count))
                bpel_invoke.save()
                bpel_invoke.save_position(Bookmark(child.parent,1,1,-1,-1))
                create_link('callLink',child,bpel_invoke,Bookmark(child.parent,1,1,-1,-1))
                flag_link = 0
                for subele in bpel_receive_data:
                    for bpel_ele in bpel_receive_data[subele]:
                        ele_data = str(bpel_ele)
                        ele_data = re.sub('(\[)|(\])|(\')','',ele_data)
                        bpel_receive_list = []
                        bpel_receive_list = ele_data.split(',')
                        receive_operation_type = ""
                        receive_port_type = ""
                        for receive_data in bpel_receive_list:
                            if 'portType:' in receive_data:
                                receive_port_type = receive_data[receive_data.find(':')+1:]
                            elif 'operation:' in receive_data:
                                receive_operation_type = receive_data[receive_data.find(':')+1:]
                        if port_type == receive_port_type and operation_type == receive_operation_type:  
                            file_name = wsdl_obj_reference[subele].parent.get_path()
                            wsdl_operation = CustomObject()
                            operation_count = operation_count+1
                            self.saveObject(wsdl_operation,receive_operation_type,file_name+receive_operation_type,"WSDL_Operation",wsdl_obj_reference[subele].parent,file_name+"WSDL_Operation"+str(operation_count))
                            wsdl_operation.save()
                            wsdl_operation.save_position(Bookmark(subele.parent,1,1,-1,-1))
                            create_link('callLink',bpel_invoke,wsdl_operation,Bookmark(subele.parent,1,1,-1,-1))
                            create_link('callLink',wsdl_operation,wsdl_obj_reference[subele],Bookmark(subele.parent,1,1,-1,-1))
                            flag_link =1
                            break
                    if flag_link == 1:
                        break
        CAST.debug('End!!')
        '''               
        for child in bpel_file_data:
            for subchild in bpel_file_data[child]:
                CAST.debug(subchild+"->")
                for j in bpel_file_data[child][subchild]:
                    CAST.debug(str(j))           
        #for child in wsdl_file_data:
            #for subchild in wsdl_file_data[child]:
        #    CAST.debug(str(wsdl_file_data[child]))
        '''
        pass
if __name__ == '__main__':
    '''
    bpel = BpelExtension()
    bpel.start_analysis()
    '''
    pass