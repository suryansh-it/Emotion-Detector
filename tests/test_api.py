from app import app

from unittest.mock import patch
from flask_login import current_user

@patch('app.current_user')  

def test_post_api_endpoint(mock_current_user):

    # Set up the mock to simulate an authenticated user
    mock_current_user.is_authenticated = True
    mock_current_user.id = 1  # Or any valid user ID

    with app.test_client() as c:
        #with : creating temporary connection with test client ; c: closes connection once test is finished
        
        response = c.post('/capture', json={'image_data': 'sample_base64_string'}) #can pass a json dir. is required
        #as this endpoint needed img data to be passed
        
        json_response= response.get_json()
        assert response.status_code == 201

        #to check if the specific conditions are met for testing , ex : message
        assert json_response['message']== 'Image captured successfully'
        
