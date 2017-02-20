import cast.application
import logging
import ast
import re


class ExtensionApplication(cast.application.ApplicationLevelExtension):

    def end_application(self, application):
        logging.debug("running code at the end of an application")
        list1 = []
        for line in self.get_intermediate_file('file.txt'):
            list1.append(line)
        list2 = []
        for i in list1 :
            list2.append(ast.literal_eval(i))
        resourceReferences = list(application.search_objects(category='BPEL_Invoke', load_properties=False))
        resourceReferences1 = list(application.search_objects(category='JV_METHOD', load_properties=False))
        for i in resourceReferences1 :
            for j in list2 :
                for k in j :
                    if (re.search('(?:\w+\.'+i.get_name()+'\(|\w+\.'+i.get_name()+'\s+\()', j[k])) : 
                        for y in resourceReferences :
                            #logging.debug( y.get_fullname())
                            if '--' in y.get_fullname():
                                if str(k) == y.get_fullname().split("--")[1] :
                                    cast.application.create_link("callLink",y,i,bookmark=None)
                                    logging.debug( y.get_fullname())
                        #logging.debug("Invoke name : "+ str(k))
                        #logging.debug("java object name"+ str(i))

        logging.debug("DONE!")
