import sys
import os

sys.path.insert(0, os.path.abspath('app'))
import app as module_app
from models import db, Job, Employee

def run_tests():
    app = module_app.app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # Test Login GET
            response = client.get('/')
            assert response.status_code == 200, f"Login GET failed: {response.status_code}"
            
            # Test Login POST (Employee)
            response = client.post('/', data={
                'email': 'employee@siliconmango.in',
                'password': 'password'
            }, follow_redirects=True)
            assert response.status_code == 200, "Login POST Employee failed"
            assert b'Employee Dashboard' in response.data or b'Set Home Location' in response.data
            
            # Set Home GET
            response = client.get('/set-home')
            assert response.status_code == 200, "Set Home GET failed"
            
            # Set Home POST
            response = client.post('/set-home', data={
                'latitude': '28.6139',
                'longitude': '77.2090'
            }, follow_redirects=True)
            assert response.status_code == 200, "Set Home POST failed"
            
            # Search Jobs GET
            response = client.get('/search-jobs?q=search jobs near me')
            assert response.status_code == 200, "Search Jobs GET failed"
            
            client.get('/logout')
            
            # Test Login POST (Employer)
            response = client.post('/', data={
                'email': 'employer@siliconmango.in',
                'password': 'password'
            }, follow_redirects=True)
            assert response.status_code == 200, "Login POST Employer failed"
            assert b'Employer Dashboard' in response.data
            
            # Create Job GET
            response = client.get('/create-job')
            assert response.status_code == 200, "Create Job GET failed"
            
            # Create Job POST
            response = client.post('/create-job', data={
                'title': 'Test Job',
                'short_description': 'A short desc',
                'description': 'Full description',
                'latitude': '28.6140',
                'longitude': '77.2091'
            }, follow_redirects=True)
            assert response.status_code == 200, "Create Job POST failed"
            
            # Re-test employee to check search finds the job
            client.get('/logout')
            client.post('/', data={
                'email': 'employee@siliconmango.in',
                'password': 'password'
            }, follow_redirects=True)
            
            response = client.get('/search-jobs?q=search jobs near me')
            assert b'Test Job' in response.data, "Job not found in search results"
            
            print("All endpoint tests passed!")

if __name__ == '__main__':
    run_tests()
