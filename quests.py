import json
import logging


class Quest:
    def __init__(self, routes):
        self.routes = routes
        self.route_name = ''

    def get_state(self):
        return {
            'route': self.route_name
        }

    def set_state(self, state):
        if 'route' in state:
            self.route_name = state['route']

    def next_question(self, answer):
        if not answer:
            self.route_name = 'start'
        elif 'next_route' in answer:
            self.route_name = answer['next_route']
        else:
            self.route_name = None

        if self.route_name:
            return self.routes[self.route_name]
        else:
            return None

    def get_current_route(self):
        return self.routes[self.route_name]

    def clear(self):
        self.route_name = ''

    def get_result_string(self):
        return 'The End'

    def get_result_image(self):
        return None


class Quests:
    def __init__(self):
        self.quest_description = ''
        self.start_message = ''
        self.routes = {}
        self.quests = {}
        self.quest_filename = 'quest.json'
        self.storage_filename = 'storage.json'
        self.load_quest()
        self.load_state()

    def get_quest_description(self):
        return self.quest_description

    def get_start_message(self):
        return self.start_message

    def start_quest(self, chat_id):
        if chat_id not in self.quests:
            self.quests[chat_id] = Quest(self.routes)
        self.quests[chat_id].clear()
        self.save_state()
        return self.quests[chat_id]

    def finish_quest(self, chat_id):
        if chat_id in self.quests:
            del self.quests[chat_id]
        self.save_state()

    def get_quest(self, chat_id):
        if chat_id in self.quests:
            return self.quests[chat_id]
        else:
            return None

    def next_question(self, chat_id, answer):
        route = None
        quest = self.get_quest(chat_id)
        if quest:
            route = quest.next_question(answer)
            self.save_state()
        return route

    def process_answer(self, chat_id, text):
        result = None
        quest = self.get_quest(chat_id)
        if quest:
            current_route = quest.get_current_route()
            if current_route:
                for answer in current_route['answers']:
                    if answer['text'].lower() == text.lower():
                        result = answer
        return result

    def load_state(self):
        state = None
        try:
            with open(self.storage_filename, 'r') as f:
                state = json.load(f)
        except IOError as e:
            logging.error(f'Ошибка восстановлении состояния квеста при открытии файла {self.storage_filename}, {e}')
        except json.decoder.JSONDecodeError as e:
            logging.error(f'Ошибка восстановлении состояния квеста при декодировании файла {self.storage_filename}, {e}')

        if state:
            logging.info('load_state: ' + str(state))
            for item in state:
                chat_id = item['chat_id']
                if chat_id not in self.quests:
                    self.quests[chat_id] = Quest(self.routes)
                self.quests[chat_id].set_state(item['quest'])

    def save_state(self):
        state = []
        for chat_id in self.quests:
            quest = self.quests[chat_id]
            state.append({
                'chat_id': chat_id,
                'quest': quest.get_state()
            })
        logging.info('save_state: ' + str(state))

        try:
            with open(self.storage_filename, 'w') as f:
                json.dump(state, f)
        except IOError as e:
            logging.error(f'Ошибка сохранения состояния квеста при открытии файла {self.storage_filename}, {e}')

    def load_quest(self):
        try:
            with open(self.quest_filename, 'r') as f:
                data = json.load(f)
                self.quest_description = data['quest_description']
                self.start_message = data['start_message']
                self.routes = data['routes']
        except IOError as e:
            logging.error(f'Ошибка загрузки квеста при открытии файла {self.quest_filename}, {e}')
        except json.decoder.JSONDecodeError as e:
            logging.error(f'Ошибка загрузки квеста при декодировании файла {self.quest_filename}, {e}')
