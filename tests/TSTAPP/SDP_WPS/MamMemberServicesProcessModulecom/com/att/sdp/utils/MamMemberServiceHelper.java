
package com.att.sdp.utils;

import java.util.Iterator;
import java.util.List;
import java.util.Random;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;


import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import sbc.lightspeed.sdp.wps.SdpHelper;
import commonj.sdo.DataObject;

public class MamMemberServiceHelper {

	public static String TN_KEY_SELECTOR = "TN";
	public static String MAILBOXINVARIANTID_KEY_SELECTOR = "MAILBOXINVARIANTID";
	public static String ADD_OPERATION_SELECTOR = "ADD";
	public static String DELETE_OPERATION_SELECTOR = "DELETE";
	public static String MAILBOX_OBJECT_SELECTOR = "MAILBOX";
	public static String MEMBERPROFILE_OBJECT_SELECTOR = "MEMBERPROFILE";
	public static String MAILBOXMEMBER_STR_SEARCHTYPE = "mailboxMembers";
	public static String MAILBOXTN_STR_SEARCHTYPE = "mailboxTNs";
   static Logger logger = LogManager.getLogger(MamMemberServiceHelper.class);
	public static final String MAM_TIMEDELAY_CONFIG_XML_FILE = "com/att/sdp/bprocess/MamMemberServices_TimeDelay_config.xml";
	
	public static void modifyMemberProfileOrMailbox(DataObject SdpOrder, String memberId, String keySelector, 
			String operationSelector, Object value, String objecctSelector) { 
		
		java.util.List lstMemberProfile = null, lstAccountMailboxes = null, lstMailboxTns = null, lstMailboxMembers = null;
		java.util.Iterator iterMemProfile = null, iterAccountMailbox = null, iterMailboxTn = null;

		DataObject dataobjMemProfTemp = null;
		DataObject memberProfile = null;
		DataObject accountMailboxTemp = null;
		DataObject accountMailbox = null;
		DataObject mailboxTnTemp = null;
		DataObject mailboxTn = null;
		DataObject mailboxMember = null;
		
		String strMemberId = null;
		String strTn = null;
		String strMailboxInvariantId = null;
		
		
		
		if ( SdpOrder!=null && memberId!=null && keySelector!=null && operationSelector!=null && value!=null 
				&& objecctSelector!=null) 
		{ 
			if (objecctSelector.equalsIgnoreCase(MEMBERPROFILE_OBJECT_SELECTOR))
			{

				//Get the list of member proflies from the SdpOrder object
				lstMemberProfile = SdpOrder.getList(SdpHelper.MEMBERPROFILE_LIST_PATH.replace('.', '/'));
				
				if(lstMemberProfile != null)
				{	
					iterMemProfile = lstMemberProfile.iterator();
	
					//Loop through for each member profile
					while (iterMemProfile.hasNext()) {
						dataobjMemProfTemp = (DataObject) iterMemProfile.next();
					
						strMemberId = dataobjMemProfTemp.getString(SdpHelper.MEMBERPROFILE_MEMBERID);

						if (strMemberId != null && strMemberId.equalsIgnoreCase(memberId)) {
							memberProfile = dataobjMemProfTemp;
							break;
						}
					}
				}	
				
				if (memberProfile!=null)
				{
					if (operationSelector.equalsIgnoreCase(ADD_OPERATION_SELECTOR))
					{
						if (keySelector.equalsIgnoreCase(MAILBOXINVARIANTID_KEY_SELECTOR))
						{
							memberProfile.setString(SdpHelper.MEMBERPROFILE_MAILBOXINVARIANTID, value.toString());
							
						}
						else if (keySelector.equalsIgnoreCase(TN_KEY_SELECTOR))
						{
							java.util.List lstSubMBoxTNs = memberProfile.getList(SdpHelper.MEMBERPROFILE_MAILBOX_TNS);
							if(!isTnExistsInList(lstSubMBoxTNs, (DataObject) value))
							{
								lstSubMBoxTNs.add((DataObject)value);
							
							}
							
						}
						
					}
					else if (operationSelector.equalsIgnoreCase(DELETE_OPERATION_SELECTOR))
					{
						if (keySelector.equalsIgnoreCase(MAILBOXINVARIANTID_KEY_SELECTOR))
						{
							strMailboxInvariantId = memberProfile.getString(SdpHelper.MEMBERPROFILE_MAILBOXINVARIANTID);
							
							if (strMailboxInvariantId.equalsIgnoreCase(value.toString()))
							{
								memberProfile.setString(SdpHelper.MEMBERPROFILE_MAILBOXINVARIANTID, "-1");
						
							}
														
						}
						else if (keySelector.equalsIgnoreCase(TN_KEY_SELECTOR))
						{
							lstMailboxTns = memberProfile.getList(SdpHelper.MEMBERPROFILE_MAILBOX_TNS);
							
							int intTNCounter = 0;
							
							if (lstMailboxTns!=null)
							{
								iterMailboxTn = lstMailboxTns.iterator();
								
								while (iterMailboxTn.hasNext())
								{
									mailboxTnTemp = (DataObject) iterMailboxTn.next();
									
									strTn = mailboxTnTemp.getString(SdpHelper.MEMBERPROFILE_MEMBER_TN);
									
									if (strTn!= null && strTn.equalsIgnoreCase(value.toString()))
									{
										mailboxTn = mailboxTnTemp;
										
										lstMailboxTns.remove(intTNCounter);
										break;
									}
									intTNCounter++;									
								}
								
							}
						}
						
					}
					
				}
				
			
			}
			else if (objecctSelector.equalsIgnoreCase(MAILBOX_OBJECT_SELECTOR))
			{
				
			}
			
				
		}
	
	
	}
	
	
	private static boolean isTnExistsInList(java.util.List lstLocal, DataObject ReqTN)
	{
		boolean blnTNExistsInList = false;
		Iterator itLocal = null;
		
		if(lstLocal != null && ReqTN != null)
		{
			itLocal = lstLocal.iterator();
			
			while(itLocal.hasNext())
			{
				DataObject subMBoxTn = (DataObject) itLocal.next();
				
				if(subMBoxTn != null)
				{
					if(subMBoxTn.getString("tn").equalsIgnoreCase(ReqTN.getString("tn")))
					{
						blnTNExistsInList = true;
					}
				}
			}
		}
		
		return blnTNExistsInList;
	}
	
	//*************
	
	public static DataObject getMemberProfile(DataObject sdpOrder,
			String mailboxInvariantId) {
		
		java.util.Iterator iterMemberProfiles = null;

		DataObject memberProfile = null;
		DataObject memberProfileOut = null;
		DataObject memberTN = null;
		
		String strMailboxInvariantId = null;
		
		java.util.List lstMemberProfiles = null;
		
	

		//Check if the sdp order object and other input param is not null.
		if (sdpOrder != null && mailboxInvariantId != null) {

			//Get the list of account mailboxes from the sdp order object
			lstMemberProfiles = sdpOrder.getList(SdpHelper.MEMBERPROFILE_LIST_PATH.replace('.','/'));
			iterMemberProfiles = lstMemberProfiles.iterator();

			//Loop through for each member profile
			while (iterMemberProfiles.hasNext()) {
				
				memberProfile = (DataObject) iterMemberProfiles.next();

				strMailboxInvariantId = memberProfile.getString(SdpHelper.MEMBERPROFILE_MAILBOXINVARIANTID);
					
					
				if(strMailboxInvariantId.equalsIgnoreCase(mailboxInvariantId))
				{
					memberProfileOut = SdpHelper.copySpecificBO(memberProfile);
	
					break;
				}	
			}
			
			
		}
		
		
		

		return memberProfileOut;
	}
	
	//*************
	
	public static DataObject getMailboxMemberOrMailboxTN(DataObject accountMailbox, String strSearch, String strSearchType) {
		
		java.util.List lstMailboxMembersOrMailboxTNs = null;
		Iterator itrMailboxMemberOrMailboxTNs = null;
		
		DataObject mailboxMemberOrMailboxTN = null;
		DataObject mailboxMemberOrMailboxTNOut = null;
		
		String memberIdOrTn = null;
		
		
		
		if (accountMailbox != null && strSearch != null && strSearchType != null)
		{
			strSearch = strSearch.trim();
			
			if (strSearchType.equalsIgnoreCase(MAILBOXMEMBER_STR_SEARCHTYPE))
			{
				lstMailboxMembersOrMailboxTNs = accountMailbox.getList(SdpHelper.VOIP_MAILBOX_MEMBERS);
			
				itrMailboxMemberOrMailboxTNs = lstMailboxMembersOrMailboxTNs.iterator();
				
		
			}
			else if (strSearchType.equalsIgnoreCase(MAILBOXTN_STR_SEARCHTYPE))
			{
				lstMailboxMembersOrMailboxTNs = accountMailbox.getList(SdpHelper.VOIP_MAILBOXTNS);
				
				itrMailboxMemberOrMailboxTNs = lstMailboxMembersOrMailboxTNs.iterator();
				
		
			}
			
			while(itrMailboxMemberOrMailboxTNs != null && itrMailboxMemberOrMailboxTNs.hasNext())
			{
				mailboxMemberOrMailboxTN = (DataObject)itrMailboxMemberOrMailboxTNs.next();
				
		
								
				if (mailboxMemberOrMailboxTN!=null)
				{
					if (strSearchType.equalsIgnoreCase(MAILBOXMEMBER_STR_SEARCHTYPE))
					{
						memberIdOrTn = mailboxMemberOrMailboxTN.getString(SdpHelper.CVOIP_MAILBOX_MEMBERID).trim();
					}
					else if (strSearchType.equalsIgnoreCase(MAILBOXTN_STR_SEARCHTYPE))
					{
						memberIdOrTn = mailboxMemberOrMailboxTN.getString(SdpHelper.CVOIP_MAILBOX_TN).trim();
					}

					if (memberIdOrTn.equalsIgnoreCase(strSearch))
					{
						mailboxMemberOrMailboxTNOut = SdpHelper.copySpecificBO(mailboxMemberOrMailboxTN);
						
		
						
						break;
					}
				}
				
			}
		}
		
		
		
		
		return mailboxMemberOrMailboxTNOut;
	}
	
	public static void updateMailboxTN(DataObject sdpAccountMailbox, DataObject sdpMailboxTN)
	{
		java.util.List lstMailboxTNs = null;
		
		Iterator iterMailboxTNs = null;

		DataObject mailboxTN = null;
		
		String strTN = null;
		String strTNName = null;
		String tmpStrTNName = null;
		
		
		
		if (sdpAccountMailbox != null && sdpMailboxTN != null)
		{
			lstMailboxTNs = sdpAccountMailbox.getList(SdpHelper.VOIP_MAILBOXTNS);
			strTN = sdpMailboxTN.getString(SdpHelper.CVOIP_MAILBOX_TN);
			strTNName = sdpMailboxTN.getString(SdpHelper.CVOIP_MAILBOX_TNNAME);
			
		
			
			if (lstMailboxTNs.size() > 0 && strTN != null && strTN.trim().length() > 0 
					&& strTNName != null && strTNName.trim().length() > 0)
			{
				iterMailboxTNs = lstMailboxTNs.iterator();
				
		
				
				while (iterMailboxTNs.hasNext())
				{
					mailboxTN = (DataObject)iterMailboxTNs.next();
					
		
					
					if (mailboxTN != null && strTN.equalsIgnoreCase(mailboxTN.getString("tn")))
					{
		
						
						tmpStrTNName = mailboxTN.getString(SdpHelper.CVOIP_MAILBOX_TNNAME);					
						//if (tmpStrTNName == null || tmpStrTNName.trim().length() == 0)
						//{
						mailboxTN.setString(SdpHelper.CVOIP_MAILBOX_TNNAME,strTNName);
							
		
						break;
						//}
					}
				}
			}
			
		}
		
	}
	
	public static void updateMemberTN(DataObject sdpMemberProfile, DataObject sdpMemberTN)
	{
		java.util.List lstMemberTNs = null;
		Iterator iterMemberTNs = null;
		
		DataObject memberTN = null;
		
		String strTN = null;
		String strTNName = null;
		String tmpStrTNName = null;
		
		
		
		if (sdpMemberProfile != null && sdpMemberTN != null)
		{
			lstMemberTNs = sdpMemberProfile.getList(SdpHelper.MEMBERPROFILE_MEMBER_TNS);
			strTN = sdpMemberTN.getString(SdpHelper.MEMBERPROFILE_MEMBER_TN);
			strTNName = sdpMemberTN.getString("tnName");
			
		
			
			if (lstMemberTNs.size() > 0 && strTN != null && strTN.trim().length() > 0 
					&& strTNName != null && strTNName.trim().length() > 0)
			{
				iterMemberTNs = lstMemberTNs.iterator();
				
		
				
				while (iterMemberTNs.hasNext())
				{
					memberTN = (DataObject)iterMemberTNs.next();
					
		
					
					if (memberTN != null && strTN.equalsIgnoreCase(memberTN.getString("tn")))
					{
		
						
						tmpStrTNName = memberTN.getString("tnName");					
						//if (tmpStrTNName == null || tmpStrTNName.trim().length() == 0)
						//{
						memberTN.setString("tnName",strTNName);
							
		
						break;
						//}
					}
				}
			}
		
		}
		
		
		
	}
	
	public static long getTimeDelayMilliSeconds()
	{
		String strSeconds = null;
		long seconds = 0;
		 		 			  
		
		try
		{
        
            
			InputSource in = new InputSource(
            MamMemberServiceHelper.class.getClassLoader().getResourceAsStream("com/att/sdp/utils/config.xml"));
            DocumentBuilderFactory docBuilderFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();
			Document doc = docBuilder.parse (in);
                               
			NodeList nodeList = doc.getElementsByTagName("TIMEDELAY_IN_MILLISECONDS");
         	Element element = (Element)nodeList.item(0);
         	NodeList textNodeList = element.getChildNodes();
            
            strSeconds = ((Node)textNodeList.item(0)).getNodeValue().trim();
                               
            seconds = Long.parseLong(strSeconds);
 		}
		catch (Exception ex)
		{
		logger.error("Caught Exception" + ex);
		}
		
		
		return seconds;
	}
	
	public static String getEmailAddress(String TN){

		String random = "";
		Random randomObj = new Random();
		String emailAddress = null;
		int noOfDigits = 4;
		
		
		if (TN != null)
		{
			//Generating random number
			for(int counter = 0; counter < noOfDigits; counter++)
			{
				int temp = randomObj.nextInt(9);	
				random = random.concat(java.lang.String.valueOf(temp));
			}
			emailAddress = TN + random;
		
		}
		
		
		
		return emailAddress;
	}
	
	public static void updateMemberProfileMemberTName(DataObject sdpOrder, DataObject TN)
	{
		List lstMemberProfile = null;
		List lstMemberTNs = null;
		
		Iterator itrMemberProfile = null;
		Iterator itrMemberTNs = null;
		
		DataObject memberProfile = null;
		DataObject memberTN = null;
		
		String strTN = null;
		String strMemberTN = null;
		String strTNName = null;
		
		lstMemberProfile = sdpOrder.getList(SdpHelper.MEMBERPROFILE_LIST_PATH.replace('.','/'));
		itrMemberProfile = lstMemberProfile.iterator();	
		
		
		
		strTN = TN.getString(SdpHelper.CVOIP_MAILBOX_TN);
		strTNName = TN.getString(SdpHelper.CVOIP_MAILBOX_TNNAME);
		
		if (strTN != null && strTN.trim().length() > 0 && lstMemberProfile.size() > 0)
		{
			while(itrMemberProfile.hasNext())
			{
				memberProfile = (DataObject)itrMemberProfile.next();
				
				if ( memberProfile!=null )
				{
					lstMemberTNs = memberProfile.getList(SdpHelper.MEMBERPROFILE_MEMBER_TNS);
					itrMemberTNs = lstMemberTNs.iterator();
					
					while(itrMemberTNs.hasNext())
					{
						memberTN = (DataObject)itrMemberTNs.next();
						
						if ( memberTN != null )
						{
							strMemberTN = memberTN.getString(SdpHelper.MEMBERPROFILE_MEMBER_TN);
							if (strMemberTN != null && strMemberTN.equalsIgnoreCase(strTN))
							{
								memberTN.setString(SdpHelper.CVOIP_MAILBOX_TNNAME,strTNName);
								break;
							}
						}
					}
				}
					
			}
		}
		
	}
	
}
