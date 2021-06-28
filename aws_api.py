import boto3
from botocore.exceptions import ClientError
from datetime import datetime

class amazonApi:
    
    def __init__(self):
        self.pinpointClient = boto3.client('pinpoint')
        self.cognitoClient = boto3.client('cognito-idp')
        self.awsCogntioId = 'test'
        self.awsAppId = 'test'
        self.senderId = 'TESTING_USER'
        
    def sendSMSCode(self,mobile, code):
        try:
            response = self.pinpointClient.send_messages(ApplicationId=self.awsAppId, MessageRequest={
            'Addresses':{
              mobile:{'ChannelType':'SMS'}},
            'MessageConfiguration':{
              'SMSMessage':{'Body':code,'MessageType':'TRANSACTIONAL','SenderId':self.senderId}}
          })
        except ClientError as e:
            print('Error: ' + e.response['Error']['Message'])
            return e.response['Error']['Message']
        else:
            print("Message sent!")
            return "Message sent!"
            
            
    def sendEmailCode(self,email, code, location):
        emailTemplate = self.pinpointClient.get_email_template(TemplateName='Send_SMS_Code', Version='latest')
        try:
            response = self.pinpointClient.send_messages(ApplicationId=self.awsAppId, MessageRequest={
                'Addresses':{
                email:{'ChannelType':'EMAIL'}},
                'MessageConfiguration':{
                    'EmailMessage':{'FromAddress':'test@gmail.com',
                    'SimpleEmail':{
                        'HtmlPart':{
                            'Data': self.getEmailTemplate(emailTemplate['EmailTemplateResponse']['HtmlPart'],email,code,location)
                        },
                        'Subject':{
                            'Data':emailTemplate['EmailTemplateResponse']['Subject']
                        }}}}})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return e.response['Error']['Message']
        else:
            print("Message sent!")
            return "Message sent!"
            
            
    def getEmailTemplate(self, template, email, code, location):
        template.replace("{User.Email}", email)
        template.replace("{User.Code}", code)
        now = datetime.now()
        template.replace("{App.Timezone}",now.strftime("%d/%m/%Y %H:%M:%S"))
        template.replace("{App.Location}", location);
        template.replace("{App.Name}", 'sadasd')
        return template
        
    

    def createUserIdentity(self, userName, nickName, email=None, mobile=None):
        attribute =  [{'Name':'nickname', 'Value' : nickName}]
        
        if email != None:
            data = [{'Name':'email' , 'Value' : email}]
            userName = email
        elif mobile != None:
            data = [{'Name' : 'phone_number' , 'Value' : mobile}]
            userName = mobile

        try:        
            response = self.cognitoClient.admin_create_user(UserPoolId = self.awsCogntioId, 
                                                Username = userName, 
                                                UserAttributes = attribute,
                                                ValidationData = data,
                                                TemporaryPassword ='Abcd1234',
                                                MessageAction = 'SUPPRESS',
                                                ForceAliasCreation = True)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return (e.response['Error']['Message'])
        else:
            print("Message sent!")
            return True
            

    def updateUserIdentity(self, userName, nickName, password, email=None, mobile=None):
        attribute =  [{'Name':'nickname', 'Value' : nickName}]
        
        if email != None:
            data = [{'Name':'email' , 'Value' : email}]
            userName = email
        elif mobile != None:
            data = [{'Name' : 'phone_number' , 'Value' : mobile}]
            userName = mobile 
             
        try:        
            response = self.cognitoClient.admin_update_user_attributes(UserPoolId = self.awsCogntioId, 
                                                Username = userName, 
                                                UserAttributes = attribute)
                                                
            response = self.cognitoClient.admin_set_user_password(UserPoolId = self.awsCogntioId, 
                                                Username = userName, 
                                                Password = password,
                                                Permanent = True)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            print("Message sent!")
            return response