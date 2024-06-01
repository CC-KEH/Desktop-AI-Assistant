import json
import requests
from credentials.notion.credentials import *

class Notion:
    def __init__(self):
        self.token = notion_token
        self.m_db_id = movie_database_id
        self.a_db_id = anime_database_id
        self.b_db_id = book_database_id
        self.t_db_id = todo_database_id
        self.version = notion_version
        self.header = {
          "Authorization": f"Bearer {self.token}",
          "Content-Type": "application/json",
          "Notion-Version": f"{self.version}"
        }
        self.watch_list_payload = {
            "parent": {
              "database_id": 'database_id'
            },
            "properties": {
              "Name": {
                "title": [
                  {
                    "text": {
                      "content": 'name'
                    }
                  }
                ]
              },
              "Genre": {
                "multi_select": [
                  {
                    "name": 'genre'
                  }
                ]
              },
              "Completed": {
                "checkbox": 'completed'
              }
            }}
        self.todo_payload = {
            "properties": {
              "Task": {
                "title": [
                  {
                    "text": {
                      "content": 'task'
                    }
                  }
                ]
              },
              "Priority": {
                "multi_select": [
                  {
                    "text": {
                      "content": 'priority'
                    }
                  }
                ]
              },
              "Completed": {
                "checkbox": 'completed'
              }
            }}

    def mapNotionResultToData(self,result,asked_for_todos):
      if asked_for_todos:
        try:
          item_id = result['id']
          properties = result['properties']
          priority = properties['Priority']['multi_select'][0]['name']
          task = properties['Task']['title'][0]['text']['content']
          completed = properties['Completed']['checkbox'] 
          return {
            'priority': priority,
            'task': task,
            'completed': completed,
            'item_id': item_id
          }
        except Exception as e:
          return None
      else:
        try:
          item_id = result['id']
          properties = result['properties']
          genre = properties['Genre']['multi_select'][0]['name']
          name = properties['Name']['title'][0]['text']['content']
          completed = properties['Completed']['checkbox'] 
          return {
            'name': name,
            'genre': genre,
            'completed': completed,
            'item_id': item_id
          }
        except Exception as e:
          return None
      
    def create_item(self, name, multivalue, asked_for, completed=False):
        if asked_for == 'todos':
          payload = self.todo_payload
          payload['properties']['Task']['title'][0]['text']['content'] = name
          payload['properties']['Priority']['multi_select'][0]['text']['content'] = multivalue
          payload['properties']['Completed']['checkbox'] = completed
        
        else:
          payload = self.watch_list_payload
          payload['properties']['Name']['title'][0]['text']['content'] = name
          payload['properties']['Genre']['multi_select'][0]['name'] = multivalue
          payload['properties']['Completed']['checkbox'] = completed

          if asked_for == 'movies':
            payload['parent']['database_id'] = self.m_db_id
          
          elif asked_for == 'animes':
            payload['parent']['database_id'] = self.a_db_id
          
          elif asked_for == 'books':
            payload['parent']['database_id'] = self.b_db_id
          


        url = f'https://api.notion.com/v1/pages'
        r = requests.post(url, headers=self.header, data=json.dumps(payload))

        asked_for = True if asked_for == 'todos' else False
        movie = self.mapNotionResultToData(r.json(),asked_for)
        return movie
    
    def get_data(self,asked_for):
        if asked_for == 'todos':
          url = f'https://api.notion.com/v1/databases/{self.t_db_id}/query'
        elif asked_for == 'movies':
          url = f'https://api.notion.com/v1/databases/{self.m_db_id}/query'
        elif asked_for == 'animes':
          url = f'https://api.notion.com/v1/databases/{self.a_db_id}/query'
        elif asked_for == 'books':
          url = f'https://api.notion.com/v1/databases/{self.b_db_id}/query'
          
        r = requests.post(url, headers=self.header)

        result_dict = r.json()
        list_result = result_dict['results']
        data = []
        asked_for = True if asked_for == 'todos' else False
        for record in list_result:
          data_dict = self.mapNotionResultToData(record, asked_for)
          data.append(data_dict)
        return data
      
    def get_item_id(self,item_name,asked_for):
      if asked_for == 'todos':
        todos = self.get_data('todos')
        for todo in todos:
          if todo['task'] == item_name:
            return todo['item_id']
          
      elif asked_for == 'movies':
        movies = self.get_data('movies')
        for movie in movies:
          if movie['name'] == item_name:
            return movie['item_id']
      
      elif asked_for == 'animes':
        animes = self.get_data('animes')
        for anime in animes:
          if anime['name'] == item_name:
            return anime['item_id']
          
      elif asked_for == 'books':
        books = self.get_data('books')
        for book in books:
          if book['name'] == item_name:
            return book['item_id']
      
    def update_item(self, item, asked_for):
      
      if asked_for == 'todos':
        item_id = self.get_item_id(item['task'],'todos')
        url = f'https://api.notion.com/v1/pages/{item_id}'
        self.todo_payload['properties']['Task']['title'][0]['text']['content'] = item['task']
        self.todo_payload['properties']['Priority']['multi_select'][0]['text']['content'] = item['priority']
        self.todo_payload['properties']['Completed']['checkbox'] = item['completed']
        r = requests.patch(url, headers={
        "Authorization": f"Bearer {self.token}",
        "Notion-Version": self.version,
        "Content-Type": "application/json"
        }, data=json.dumps(self.todo_payload))
        
      else:
        self.watch_list_payload['properties']['Name']['title'][0]['text']['content'] = item['name']
        self.watch_list_payload['properties']['Genre']['multi_select'][0]['name'] = item['genre']
        self.watch_list_payload['properties']['Completed']['checkbox'] = item['completed']

        if asked_for == 'movies':
          movie_id = self.get_item_id(item['name'],'movies')
          url = f'https://api.notion.com/v1/pages/{movie_id}'

        elif asked_for == 'animes':
          anime_id = self.get_item_id(item['name'],'animes')
          url = f'https://api.notion.com/v1/pages/{anime_id}'

        elif asked_for == 'books':
          book_id = self.get_item_id(item['name'],'books')
          url = f'https://api.notion.com/v1/pages/{book_id}'
        
        r = requests.patch(url, headers={
        "Authorization": f"Bearer {self.token}",
        "Notion-Version": self.version,
        "Content-Type": "application/json"
        }, data=json.dumps(self.watch_list_payload))
      asked_for = True if asked_for == 'todos' else False
      movie = self.mapNotionResultToData(r.json(),asked_for)
      return movie
          
          
if __name__ == "__main__":
    notion = Notion()

    task = {
      'task': 'task2',
      'priority': 'medium',
      'completed': True
    }
    
    updatedMovie = notion.update_item(item=task, asked_for='todos')