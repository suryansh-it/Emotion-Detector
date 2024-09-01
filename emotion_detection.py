import requests
import json

def emotion_detector(text_to_analyze):


    URL =  'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    
# Make the POST request to the Watson API
    response = requests.post(URL, json= input_json , headers= headers, verify=False , timeout=60)

# Check if the response status is OK (status code 200)
    if response.status_code == 200 :

 # Convert the response text into a dictionary
        response_data = json.loads(response.text)

 # Extract the emotions and their scores
        emotions = response_data['document']['emotion']
        anger_score = emotions['anger']
        disgust_score = emotions['disgust']
        fear_score = emotions['fear']
        joy_score = emotions['joy']
        sadness_score = emotions['sadness']



# Find the dominant emotion (the one with the highest score)
        dominant_emotion = max(emotions, key=emotions.get)


 # Return the emotions and the dominant emotion
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }

    else:
        # Handle errors, such as timeouts or issues with the API
        return {"error": "Failed to connect to Watson NLP API"}


    # response_data = response.json()
    # return response_data.get('text')
   


if __name__ == "__main__" :
    text_input = input("enter text to detect emotion : ")
    detect_emotion = emotion_detector(text_input)
    print(f"emotion : {detect_emotion}")