
"""

@author: Shariyar

"""
import xml.etree.ElementTree

def updateContent(child: xml.etree.ElementTree, content:str):
    if (child.text is not None):
        content=content+child.text+" "
    if (child.tail is not None):
        content=content+child.tail+ " "
    return content
            
    
# Funnction to parse regulations only
def parseRegulation(root: xml.etree.ElementTree):
    '''
      Parses regulation based xml file
      :param root: xml node of type xml.etree.ElementTree
      :returns dictionary of keys and values
    '''
    xRefXternal=list()
    content=""
    modifiedYear="NA"
    regYear="NA"
    consolidationYear="NA"
    #dt=""
    #modFlag=False
    xmlDict=dict()
    
    
    for child in root.iter():
        #print (child.tag,child.text,child.tail)
        if child.tag=="XRefExternal":
            txt=""
            if child.text is None:
                if child[0].tail is not None:
                    txt=child[0].tail
                else:
                     txt=child[0].text
            else:
                txt=child.text
            xRefXternal.append(txt)
            content=updateContent(child,content)
            #content+=txt+" "
       # get modifed date 
        elif ("ModifiedDate" in child.tag):
         
            dateTag=child[0]
            #print(date[1].text)
            modifiedYear=dateTag[0].text
        elif (child.tag=="RegistrationDate"):
            dateTag=child[0]
            #print(date[1].text)
            regYear=dateTag[0].text
        elif (child.tag=="ConsolidationDate"):
            dateTag=child[0]
            #print(date[1].text)
            consolidationYear=dateTag[0].text 
        elif (child.tag=="InstrumentNumber"):
            xmlDict["instrumentNumber"]=child.text
        elif (child.tag=="ShortTitle"):
            xmlDict["shorttitle"]=child.text
        elif (child.tag=="RegulationMaker"):
            xmlDict["regulationmaker"]=child.text
        elif (child.tag=="LongTitle"):
            xmlDict["longtitle"]=child.text 
            content+=child.text+". "
        elif (child.tag=="TitleText"):
            if child.text is None:
                if len(child)>0  and child[0].text is not None:
                    content+=child[0].text+". "
            else:
                content+=child.text+". "
       
            
        elif child.tag=="MM" or child.tag=="DD" or child.tag=="YYYY"  or child.tag=="Label":
            continue;
        elif child.tag=="Repealed":
            print (child.text)
            return None # igonre reglations with repeal keywords
            
        else:
            content=updateContent(child,content)
            #print(child.tag,child.text)
            '''if (child.text is not None):
            
                content=content+child.text+" "
            if (child.tail is not None):
                content=content+child.tail+ " "'''
                
           
    xmlDict["modifiedyear"]=modifiedYear
    xmlDict["registrationyear"]=regYear
    xmlDict["consolidationyear"]=consolidationYear
    xmlDict["xrefxternal"]=xRefXternal
    xmlDict["content"]=content
    
    
    return (xmlDict)
        
##################
#    Acts Parser
#################        

def parseAct(root: xml.etree.ElementTree):
    '''
      Parses regulation based xml file
      :param root: xml node of type xml.etree.ElementTree
      : returns dictionary of keys and values
    '''
    xRefXternal=list()
    xRefInternal=list()
    content=""
    regYear="NA"
    consolidationYear="NA"
    regnalYears="NA"
     
    #dt=""
    #modFlag=False
    xmlDict=dict()
    
    
    for child in root.iter():
        #print (child.tag,child.get("stage"))
        if child.tag=="XRefExternal":
            txt=""
            if child.text is None:
                if child[0].tail is not None:
                    txt=child[0].tail
                else:
                     txt=child[0].text
            else:
                txt=child.text
            xRefXternal.append(txt)
            #content+=txt+" "
            content=updateContent(child,content)
       # get modifed date 
       
        elif ("Stages"==child.tag and child.get("stage")=="assented-to"):
            
            dateTag=child[0]
            #print(date[1].text)
            regYear=dateTag[0].text
        elif (child.tag=="Stages" and child.get("stage")=="consolidation"):
            dateTag=child[0]
            #print(date[1].text)
            consolidationYear=dateTag[0].text
        elif (child.tag=="RegnalYear"):
            regnalYears=child.text
        elif (child.tag=="ConsolidatedNumber"):
            xmlDict["ConsolidatedNumber"]=child.text
        elif (child.tag=="ShortTitle"):
            xmlDict["shorttitle"]=child.text
        elif (child.tag=="RunningHead"):
            xmlDict["runninghead"]=child.text
        elif (child.tag=="ConsolidatedNumber"):
            xmlDict["consolidatednumber"]=child.text
        elif (child.tag=="AnnualStatuteNumber"):
            xmlDict["annualstatutenumber"]=child.text
        elif (child.tag=="XRefInternal"):
            xRefInternal.append(child.text)
        elif (child.tag=="LongTitle"):
            if (child.text is not None): # funny sometimes there are two long titles 
                xmlDict["longtitle"]=child.text 
                content+=child.text+". "
        elif (child.tag=="TitleText"):
            if child.text is None:
                if len(child)>0  and child[0].text is not None:
                    content+=child[0].text+". "
            else:
                content+=child.text+". "
       
       
            
        elif child.tag=="MM" or child.tag=="DD" or child.tag=="YYYY"  or child.tag=="Label":
            continue;
        elif child.tag=="Repealed":
            print (child.text)
            return None # igonre reglations with repeal keywords
            
            
        else:
            #print(child.tag,child.text)
            content=updateContent(child,content)
            '''if (child.text is not None):
            
                content=content+child.text+" "
            if (child.tail is not None):
                content=content+child.tail+ " "'''
                
    
    
    xmlDict["registrationyear"]=regYear
    xmlDict["consolidationyear"]=consolidationYear
    xmlDict["regnalyears"]=regnalYears
    xmlDict["xrefxternal"]=xRefXternal
    xmlDict["xrefinternal"]=xRefInternal
    xmlDict["content"]=content
    
    
    return (xmlDict)
        
        
        
# Unit test: usage method
import os
import xml.etree.ElementTree as ET
directory="..somepath/regs"
#directory="..somepaths/acts"
count=0
n=0
for filename in os.listdir(directory):
    if filename.endswith(".xml") and (not filename.startswith("SI-") and filename=="SOR-2009-317.xml"):
        #print (filename)
        path=os.path.join(directory, filename)
        tree=ET.parse(path)
        d=parseRegulation(tree.getroot())
		print (d)
        n=n+1
#       # d=parseAct(tree.getroot())
#        #if (d==None):
#         #   print (filename)
#          #  count =count +1
#        print(d)
#print(count)
#print (n)
#       # d=parseAct(tree.getroot())
        #print(d)