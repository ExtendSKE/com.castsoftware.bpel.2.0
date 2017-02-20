import cast.application
import logging
import ast
import re


class ExtensionApplication(cast.application.ApplicationLevelExtension):

    def end_application(self, application):
        logging.debug("running code at the end of an application")
        logging.debug("*************")
        list1 = []
        for line in self.get_intermediate_file('file.txt'):
            list1.append(line)
        list2 = []
        for i in list1 :
            list2.append(ast.literal_eval(i))
        resourceReferences = list(application.search_objects(category='BPEL_Invoke', load_properties=False))
        resourceReferences1 = list(application.search_objects(category='JV_METHOD', load_properties=False))
        for i in resourceReferences1 :
        #if i.get_type() == "JV_METHOD" :
            for j in list2 :
                for k in j :
                    #logging.debug("$$$$$$$$$$")
                    #logging.debug(j[k].find( i.get_name()))
                    #if j[k].find( i.get_name()) != -1 :
                    if (re.search('(?:\w+\.'+i.get_name()+'\(|\w+\.'+i.get_name()+'\s+\()', j[k])) : 
                        for y in resourceReferences :
                            #logging.debug( y.get_fullname())
                            if y.get_fullname().find('--')!=-1:
                                #logging.debug(str(k))
                                if str(k) == y.get_fullname().split("--")[1] :
                                    #logging.debug("&&&&&&&&&&&&&&&&&&&&&&&&&&")
                                    cast.application.create_link("callLink",y,i,bookmark=None)
                                    logging.debug( y.get_fullname())
                        #logging.debug("Invoke name : "+ str(k))
                        #logging.debug("java object name"+ str(i))
                        #cast.application.create_link("callLink",resourceReferences[0],i,bookmark=None)


            '''
            if i.name == "name":
                cast.application.create_link("callLink",resourceReferences[0],i,bookmark=None)
            '''
            logging.debug("DONE!")
