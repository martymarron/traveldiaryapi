from rest_framework.test import APITestCase
from rest_framework import status
from milestones.models import Diary, MileStone

# Create your tests here.

class DiaryViewSetTests(APITestCase):
    
    def setUp(self):
                
        diary1 = Diary.objects.create(title='hoge', description='Hello')
        MileStone.objects.create(diary=diary1, page_id='IIIII')
        MileStone.objects.create(diary=diary1, page_id='XXXXX')
        
        diary2 = Diary.objects.create(title='fuga', description='Good bye')
        MileStone.objects.create(diary=diary2, page_id='JJJJJ')
        MileStone.objects.create(diary=diary2, page_id='YYYYY')
            
    def test_view_list_get(self):
        
        response = self.client.get("/diaries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['title'], 'hoge')
        self.assertEqual(response.data[0]['milestones'][0]['page_id'], 'IIIII')
        self.assertEqual(response.data[0]['milestones'][1]['page_id'], 'XXXXX')

        self.assertEqual(response.data[1]['title'], 'fuga')
        self.assertEqual(response.data[1]['milestones'][0]['page_id'], 'JJJJJ')
        self.assertEqual(response.data[1]['milestones'][1]['page_id'], 'YYYYY')
        
    def test_view_list_get_with_param_title(self):

        response = self.client.get("/diaries/?title=fug")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['title'], 'fuga')
        self.assertEqual(response.data[0]['milestones'][0]['page_id'], 'JJJJJ')
        self.assertEqual(response.data[0]['milestones'][1]['page_id'], 'YYYYY')

    def test_view_list_get_with_param_description(self):

        response = self.client.get("/diaries/?description=Good")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['title'], 'fuga')
        self.assertEqual(response.data[0]['description'], 'Good bye')
        self.assertEqual(response.data[0]['milestones'][0]['page_id'], 'JJJJJ')
        self.assertEqual(response.data[0]['milestones'][1]['page_id'], 'YYYYY')

    def test_view_detail_get(self):

        response = self.client.get("/diaries/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['title'], 'fuga')
        self.assertEqual(response.data['milestones'][0]['page_id'], 'JJJJJ')
        self.assertEqual(response.data['milestones'][1]['page_id'], 'YYYYY')
        
    def test_view_list_put(self):
        
        data = {
                'title': 'piyo',
                'description': 'hoge fuga piyo',
                'milestones': [
                               {
                                'page_id': 'KKKKK'
                                },
                               {
                                'page_id': 'LLLLL'
                                }
                               ]
                }
        response = self.client.post('/diaries/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['title'], 'piyo')
        self.assertEqual(response.data['description'], 'hoge fuga piyo')
        self.assertEqual(len(response.data['milestones']), 2)
        self.assertEqual(response.data['milestones'][0]['page_id'], 'KKKKK')
        self.assertEqual(response.data['milestones'][1]['page_id'], 'LLLLL')

    def test_view_detail_put(self):
        
        response = self.client.get("/diaries/3/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['title'], 'hoge')
        self.assertEqual(response.data['milestones'][0]['page_id'], 'IIIII')
        self.assertEqual(response.data['milestones'][1]['page_id'], 'XXXXX')
 
        data = {
                'title': 'puyo',
                'description': 'hoge fuga piyo'
                }
        response = self.client.post('/diaries/3/', data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'puyo')
#         self.assertEqual(response.data['description'], 'hoge fuga piyo')
#         self.assertEqual(len(response.data['milestones']), 2)
#         self.assertEqual(response.data['milestones'][0]['page_id'], 'KKKKK')
#         self.assertEqual(response.data['milestones'][1]['page_id'], 'LLLLL')
        
# class MilestoneViewSetTests(APITestCase):
#     
#     def setUp(self):
#                
#         diary1 = Diary.objects.create(title='hoge')
#         MileStone.objects.create(diary=diary1, page_id='IIIII')
#         MileStone.objects.create(diary=diary1, page_id='XXXXX')
#         
