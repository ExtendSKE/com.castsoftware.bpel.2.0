import cast.analysers.ua
import cast.analysers.log as X
import re
from cast.analysers import CustomObject , Bookmark,create_link
import tag_checker as TC
list_wsdl_file = []
bpel_receive_data = {}
bpel_invoke_data = {}
dict_wsdl_data = {}
bpel_process_data ={}
wsdl_obj_reference = {}
class MyExtension(cast.analysers.ua.Extension):
    def __init__ (self):
        self.name = ""
        self.index = -1
        self.tags = []
        self.bpel_tag_data = {}
        self.process_list_data = []
    def start_analysis(self):
        cast.analysers.log.debug('Processing..!!')
        #cast.analysers.log.debug(os.getcwd())
    def start_file(self,file):
        #cast.analysers.ua.Extension.start_file(self,file)
        filename = file.get_path()
        X.debug(filename)
        if filename.find(".wsdl") !=-1:
            self.index = filename.rfind('\\')
            if self.index != -1:
                self.name = filename[self.index+1:]
            try:
                self.index = list_wsdl_file.index(self.name)
            except ValueError:
                self.index = -1
            if self.index ==-1:
                list_wsdl_file.append(self.name)
                wsdl_obj = CustomObject()
                bookmark = Bookmark(file,1,1,-1,-1)
                wsdl_obj.set_name(self.name)
                wsdl_obj.set_fullname(filename+self.name)
                wsdl_obj.set_type("WSDL_Process")
                wsdl_obj.set_parent(file)
                wsdl_obj.set_guid(filename+self.name)
                wsdl_obj.save()
                wsdl_obj.save_position(bookmark)
                dict_wsdl_data[wsdl_obj]=TC.cast_parser_wsdl(filename)
        elif filename.find(".bpel")!=-1:
            self.tags,self.bpel_tag_data=TC.cast_parser_bpel(filename)
            #self.process_list_data = str(self.bpel_tag_data["process"]).split(",") 
            self.name = str(self.bpel_tag_data["process"])
            self.name = re.sub('\[','',self.name)
            self.name = re.sub('\]','',self.name)
            self.name = re.sub("'",'',self.name)
            self.process_list_data = self.name.split(',')
            for j in self.process_list_data:
                if j.find('name')!=-1 and j.find('targetNamespace') ==-1:
                    self.name = j[j.find(':')+1:]
            process_obj =CustomObject()
            bookmark = Bookmark(file,1,1,-1,-1)
            process_obj.set_name(self.name)
            process_obj.set_fullname(filename+self.name)
            process_obj.set_type("BPEL_Process")
            process_obj.set_parent(file)
            process_obj.set_guid(filename+self.name)
            process_obj.save()
            process_obj.save_position(bookmark)
            bpel_process_data[process_obj] = self.process_list_data
            if len(self.bpel_tag_data["receive"])!=0:
                bpel_receive_data[process_obj] = self.bpel_tag_data["receive"]
            if len(self.bpel_tag_data["invoke"])!=0:
                bpel_invoke_data[process_obj] = self.bpel_tag_data["invoke"]
            #process_obj.set_name()                  
    def end_file(self,file):
        pass
    def end_analysis(self):
        for j in bpel_process_data:
            bpel_data =""
            for i in bpel_process_data[j]:
                if i.find("targetNamespace")!=-1:
                    bpel_data = i[i.find(':')+1:]
                    #X.debug(bpel_data)        
            for i in dict_wsdl_data:
                wsdl_data =""
                for k in dict_wsdl_data[i]:
                    if k.find("targetNamespace")!=-1:
                        wsdl_data = k[k.find(':')+1:]
                if wsdl_data == bpel_data:
                    create_link('callLink',i,j,Bookmark(i.parent,1,1,-1,-1))
                    wsdl_obj_reference[j] = i 
        for i in bpel_invoke_data:
            for j in bpel_invoke_data[i]:
                port_type=""
                op_type = ""
                tmp_list = []
                tmp_list = j.split(',')
                for k in tmp_list:
                    if k.find("portType")!=-1:
                        port_type =k[k.find(':')+1:]
                    if k.find("operation")!=-1:
                        op_type = k[k.find(':')+1:]
                #X.debug(port_type+op_type)
                flag = 0
                for k in bpel_receive_data:
                    for k1 in bpel_receive_data[k]:
                        tmp_list_1 = []
                        tmp_list_1 = k1.split(',')
                        port_type_1 = ""
                        op_type_1 = ""
                        for k2 in tmp_list_1:
                            if k2.find("portType")!=-1:
                                port_type_1 =k2[k2.find(':')+1:]
                            if k2.find("operation")!=-1:
                                op_type_1 = k2[k2.find(':')+1:]
                        if port_type ==port_type_1 and op_type == op_type_1:
                            '''
                            X.debug(str(i.parent))
                            X.debug(str(k.parent))
                            X.debug(port_type+op_type)
                            X.debug(port_type_1+op_type_1)
                            '''
                            create_link('callLink',i,wsdl_obj_reference[k],Bookmark(i.parent,1,1,-1,-1))
                            flag = 1
                            break
                    if flag == 1:
                        break
                           
    pass
if __name__ == '__main__':
    pass