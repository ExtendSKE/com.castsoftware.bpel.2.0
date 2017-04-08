import cast.analysers.log as CAST
import re
from cast.analysers import Bookmark
class QualityRule():
    
    def __init__(self):     
        self.partnerlink_name = []
        self.variable_name = []
        pass
    
    
    '''
     Quality rule Implementation of Property Id -> 1187061.
     Checking Variable name is unique in same scope.
    '''
   
    def QrOnVariableName(self,data): 
        flag = 0
        for child in data:
            for subchild in child:
                if "name:" in subchild:
                    try:
                        flag = self.variable_name.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                    if flag!=-1:
                        return True
                    else:
                        self.variable_name.append(subchild[subchild.find(':')+1:])
                
        return False    
        pass
    
    
    '''
     Quality rule Implementation of Property Id -> 1187062.
     Checking Partner link name is unique in same scope.
    '''
  
    def QrOnPartnerlinkName(self,data):  
        flag =0
        for child in data:
            for subchild in child:
                if "name:" in subchild:
                    try:
                        flag= self.partnerlink_name.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                    if flag!=-1:
                        return True
                    else:
                        self.partnerlink_name.append(subchild[subchild.find(':')+1:])   
        return False
    
    '''
     Quality rule Implementation of Property Id -> 1187063 and 1187075.
     Checking Event handler contains Atleast-one Alarm event or not
    '''
   
    def QrOnEventhanlderConflict(self,file_data):
        flag =0
        onalarm = 0
        onevent = 0
        for line in file_data:
            ref = re.search('<(.+?)eventHandlers',line)
            if not "</" in line and ref or "<eventHandlers" in line:
                flag =1
            elif flag == 1:
                ref_end = re.search("</(.+?)eventHandlers",line)
                ref_onevent = re.search("<(.+?)onEvent",line)
                ref_onalarm = re.search("<(.+?)onAlarm",line)
                if ref_end or "</eventHandlers>" in line:
                    if onevent==1 or onalarm == 1:
                        onevent=0
                        onalarm =0
                        flag =0
                    else:
                        return True
                elif ref_onevent or "onEvent" in line:
                    onevent =1
                elif ref_onalarm or "onAlarm" in line:
                    onalarm =1
            else:
                continue
        return False
        pass
    
    '''
    Quality rule Implementation of Property Id -> 1187064.
    Checking reply tag for conflict
    '''
    
    def QrOnReplyConflict(self,file_data):
        flag = 0
        topart = 0
        input_exist = 0
        for line in file_data:
            ref = re.search("<(.+?)reply",line)
            if not "</" in line and ref or "<reply" in line:
                flag = 1
            elif flag == 1:
                ref_topart = re.search("<(.+?)toPart",line)
                ref_input = re.search("<(.+?)input",line)
                ref_end = re.search("</(.+?)reply",line)
                if ref_end or "</reply" in line:
                    if topart == 1 and input_exist ==1:
                        return True
                    else:
                        flag =0
                        topart =0
                        input_exist =0
                elif ref_topart or "<topart" in line:
                    topart =1
                elif ref_input or "<input" in line:
                    input_exist = 1
                else:
                    continue            
        return False       
        pass
    
    '''
    Quality rule Implementation of Property Id -> 1187065.
    Checking Correlation set name for uniqueness  
    '''
    
    def QrOnCorrelationsetConflict(self,cor_data):
        unique_cor_data = []
        flag =0
        for child in cor_data:
            for subchild in child:
                if "name:" in subchild:
                    try :
                        flag= unique_cor_data.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                    if flag != -1:
                        return True
                    else:
                        unique_cor_data.append(subchild[subchild.find(':')+1:])
                    break
        return False
        pass
    
    
    '''
    Quality rule Implementation of Property Id -> 1187066.
    Checking variable used inside from and to tag  should be defined variable
    '''
   
    def QrOnFromToConflict(self,bpel_data):
        variable_name = []
        flag =0
        for child in bpel_data["variable"]:
            for subchild in child:
                if "name:" in subchild:
                    variable_name.append(subchild[subchild.find(':')+1:])
                    
        for child in bpel_data["from"]:
            for subchild in child:
                if "variable:" in subchild:
                    try:
                        flag = variable_name.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                    if flag!=-1:
                        continue
                    else:
                        return True
                    
        for child in bpel_data["to"]:
            for subchild in child:
                if "variable:" in subchild:
                    try:
                        flag = variable_name.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                    if flag!=-1:
                        continue
                    else:
                        return True
                        
        return False 
        pass
    
    
    '''
     Quality rule Implementation of Property Id -> 1187067.
     Checking Variable name exist '.' or not (special characters checker).
    '''
   
    def QrOnVariableNamingChecker(self,data):
        for child in data:
            for subchild in child:
                if "name:" in subchild:
                    if '.' in subchild[subchild.find(':')+1:]:
                        return True 
        return False
    
    
    '''
     Quality rule Implementation of Property Id -> 1187068.
     Checking Variable type exist or not.
    '''
   
    def QrOnVariableType(self,data):
        for child in data:
            if 'type:' in str(child) or 'messageType:' in str(child) or 'element:' in  str(child):
                continue
            else:
                return True
        return False
    
        
    '''
    Quality rule Implementation of Property Id -> 1187069.
    Checking FaultHandler contains catch or catchALL activity inside it.
    '''
   
    def QrOnFaultHandlerConflict(self,file_data):
        flag =0 
        for line in file_data:
            ref = re.search("<(.+?)faultHandlers",line)
            ref_end =re.search("</(.+?)faultHandlers",line)
            ref_catch = re.search("<(.+?)catch",line)
            if not "</" in line and ref or "<faultHandlers" in line:
                flag =1
            elif "</catch" in line or "<catch" in line or ref_catch:
                if flag == 0:
                    return True
            elif ref_end or "</faultHandlers" in line:
                if flag ==1:
                    flag =0
            else:
                continue
        return False
        pass
    
    
    '''
    Quality rule Implementation of Property Id -> 1187070.
    Checking CompensatScope should be used inside faulthandler.
    '''
   
    def QrOnCompensateConflict(self,file_data):
        flag = 0
        for line in file_data:
            ref = re.search("<(.+?)faultHandlers",line)
            ref_end = re.search("</(.+?)faultHandlers",line)
            ref_scope = re.search("<(.+?)compensateScope",line)
            if not "</" in line and ref or "<faultHandlers" in line:
                flag =1
            elif "</compensateScope" in line or "<compensateScope" in line or ref_scope:
                if flag ==0:
                    return True
            elif ref_end or "</faultHandlers" in line:
                if flag == 1:
                    flag =0
            else:
                continue
        return False              
        pass
    
    
    
    '''
     Quality rule Implementation of Property Id -> 1187071.
     Checking Partner link role exist or not.
    '''
   
    def QrOnPartnerlinkRole(self,data):  
        for child in data:
            list_data = str(child)
            if "myRole:" in list_data or "partnerRole:" in list_data:
                continue;
            else:
                return True
        return False
    
    '''
    Quality rule Implementation of Property Id -> 1187072.
    Checking inside flow tag whether link name is unique or not
    '''
   
    def QrOnFlowConflict(self,link_data):
        unique_link = []
        flag = 0
        for child in link_data:
            for subchild in child:
                if "name:" in subchild:
                    try:
                        flag = unique_link.index(subchild[subchild.find(':')+1:])
                    except:
                        flag =-1
                if flag!=-1:
                    return True
                else:
                    unique_link.append(subchild[subchild.find(':')+1:])
        return False       
        pass
    
    
    '''
    Quality rule Implementation of Property Id -> 1187073.
    Checking at least one catch or catch=all inside fault handler
    '''
   
    def QrOnFaulthandlerConstrainst(self,file_data):
        flag = 0
        catch_count = 0
        for line in file_data:
            ref = re.search("<(.+?)faultHandlers",line)
            if not "</" in line and ref or "<faultHandlers" in line:
                flag = 1
            elif flag ==1:
                ref_end=re.search("</(.+?)faultHandlers",line)
                ref_catch = re.search("<(.+?)catch",line)
                if ref_end or "</faultHandlers" in line:
                    if catch_count == 0:
                        return True
                    else:
                        flag= 0
                        catch_count =0
                elif ref_catch or "<catch" in line:
                    catch_count =1
        return False
        pass
    
    
    
    
    '''
    Quality rule Implementation of Property Id -> 1187074.
    Checking if variable attribute is present inside onevent then messsagetype or element attribute must be defined
    '''
   
    def QrOnEventConflict(self,event_data):
        for child in event_data:
            flag = 0
            for subchild in child:
                if "variable:" in  subchild:
                    flag =flag+1
                elif "messageType:" in subchild:
                    flag =flag +1
            if flag == 0 or flag ==2:
                continue
            else:
                return True
        return False 
        pass
   
    
    '''
    Quality rule Implementation of Property Id -> 1187076.
    Checking Operation name should be one in a invoke activity
    '''
   
    def QrOnOperationNameConflict(self,invoke_data):
        for child in invoke_data:
            flag =0
            for subchild in child:
                if "operation:" in subchild:
                    flag= flag+1
                if flag > 1:
                    return True
        return False            
        pass
    
   
    '''
    Calling BPEL Quality rule functions and saving violations.    
    ''' 
        
    def BpelQrImplementation(self,file,bpel_process,bpel_data,file_data):
        if self.QrOnPartnerlinkName(bpel_data['partnerLink']):
            CAST.debug("Violation on Property id 1187062....")
            bpel_process.save_violation("File_Data.patnerlink_name_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)   
        if self.QrOnPartnerlinkRole(bpel_data['partnerLink']):
            CAST.debug("Violation on Property id 1187071....")
            bpel_process.save_violation("File_Data.patnerlink_role_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)  
        if self.QrOnVariableName(bpel_data['variable']):
            CAST.debug("Violation on Property id 1187061....")
            bpel_process.save_violation("File_Data.variable_name_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnVariableNamingChecker(bpel_data['variable']):
            CAST.debug("Violation on Property id 1187067....")
            bpel_process.save_violation("File_Data.variable_name_constraints",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnVariableType(bpel_data['variable']):
            CAST.debug("Violation on Property id 1187068....")
            bpel_process.save_violation("File_Data.variable_type_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnEventhanlderConflict(file_data):
            CAST.debug("Violation on Property id 1187063 &1187075....")
            bpel_process.save_violation("File_Data.eventhandler_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
            bpel_process.save_violation("File_Data.Eventhandler_constraints",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnReplyConflict(file_data):
            CAST.debug("Violation on Property id 1187064....")
            bpel_process.save_violation("File_Data.forreply_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnCorrelationsetConflict(bpel_data["correlationSet"]):
            CAST.debug("Violation on Property id 1187065....")
            bpel_process.save_violation("File_Data.correlationset_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnFromToConflict(bpel_data):
            CAST.debug("Violation on Property id 1187066....")
            bpel_process.save_violation("File_Data.from_to_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnFaultHandlerConflict(file_data):
            CAST.debug("Violation on Property id 1187069....")
            bpel_process.save_violation("File_Data.faulthandler_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)  
        if self.QrOnCompensateConflict(file_data):
            CAST.debug("Violation on Property id 1187070....")
            bpel_process.save_violation("File_Data.compensate_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)  
        if self.QrOnFlowConflict(bpel_data["link"]):
            CAST.debug("Violation on Property id 1187072....")
            bpel_process.save_violation("File_Data.flow_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if self.QrOnFaulthandlerConstrainst(file_data):
            CAST.debug("Violation on Property id 1187073....")
            bpel_process.save_violation("File_Data.faulthandler_constraints",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        if  self.QrOnEventConflict(bpel_data["onEvent"]):
            CAST.debug("Violation on Property id 1187074....")
            bpel_process.save_violation("File_Data.onevent_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        '''
        if self.QrOnEventhanlderConflict(file_data):
            CAST.debug("Violation on Property id 1187075....")
            bpel_process.save_violation("File_Data.Eventhandler_constraints",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
        '''
        if self.QrOnOperationNameConflict(bpel_data["invoke"]):
            CAST.debug("Violation on Property id 1187076....")
            bpel_process.save_violation("File_Data.operation_name_conflict",Bookmark(file,1,1,-1,-1),additional_bookmarks=None)
                        
               
    def WsdlQrImplmentation(self,file,wsdl_process,wsdl_data):
        pass  
            
if __name__ == '__main__':
    pass
    