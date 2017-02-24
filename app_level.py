import cast.application
import logging
import ast
import re

class ExtensionApplication(cast.application.ApplicationLevelExtension):

    def end_application(self, application):
        logging.debug("Running code at the end of an Application")
        
        invokeJavaCodeList = []
        # getting data from the intermediate file and converting to the correct format before inserting in the list
        for line in self.get_intermediate_file('bpel.txt'):
            invokeJavaCodeList.append(ast.literal_eval(line))

        bpelInvokeObjectReferences = list(application.search_objects(category='BPEL_Invoke', load_properties=False))
        javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', load_properties=False))
        for javaMethodObject in javaMethodObjectReferences :
            for invoke_keys in invokeJavaCodeList :
                for javaCode in invoke_keys :
                    if (re.search('(?:\w+\.'+javaMethodObject.get_name()+'\s*\()', invoke_keys[javaCode])) : 
                        for bpelInvokeObject in bpelInvokeObjectReferences :
                            if '--' in bpelInvokeObject.get_fullname():
                                if str(javaCode) == bpelInvokeObject.get_fullname().split("--")[1] :
                                    cast.application.create_link("callLink", bpelInvokeObject, javaMethodObject, bookmark=None)
                                    logging.debug( bpelInvokeObject.get_fullname())

        logging.debug("DONE!")
        pass
if __name__ == '__main__':
    pass
