# import boto3 

# dynamodb = boto3.resource('dynamodb')

# table = dynamodb.Table('gen-ai-pdf')

# from boto3.dynamodb.conditions import Key

# def insert_data(data):
#     response = table.put_item(Item=data)

#     return response


# # def update_records_status(sessionId,result):
    
# #     response = table.update_item(
# #        Key={"sessionId": sessionId}, # to get record
            
# #        UpdateExpression="set currentStatus = :val1",
# #        ExpressionAttributeValues={
# #                                   ":val1": result,
# #                                   }, 
       
# #        ReturnValues="UPDATED_NEW" 
# #        )


# def update_records_status(sessionId,result):
#     update_expression = "SET qna = :values"  
#     # Replace 'your_list_column' with the actual name of the list column
#     expression_attribute_values = {':values': result} 
#     # Update the item in the table
#     table.update_item(Key={'sessionId': sessionId},    
#                     UpdateExpression=update_expression,     
#                     ExpressionAttributeValues=expression_attribute_values )
    
    
#     return {"succesfully updated rows"}

# def fetch_data(sessionId):
#     key_condition_expression = Key('sessionId').eq(sessionId) 

#     response = table.query(KeyConditionExpression=key_condition_expression) 
#     # # Extract the result column value from the response
#     result_column_value = response['Items'][0]['qna']
#     print("result column",result_column_value)
#     return result_column_value
