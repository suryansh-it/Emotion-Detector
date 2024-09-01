import requests

def emotion_detector(text_to_analyze):


    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json= input_json , headers= headers)
    response_data = response.json()
    return response_data.get('text')


if __name__ == "__main__" :
    text_input = input("enter text to detect emotion : ")
    detect_emotion = emotion_detector(text_input)
    print(f"emotion : {detect_emotion}")