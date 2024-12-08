import motor.motor_asyncio
from config import DB_URL, DB_NAME

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)
        
    async def set_forward(self, id, forward):
        print(forward)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'forward_id': forward}})
        print(z)

    async def get_forward(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('forward_id', None)

    # session
    async def set_session(self, id, session_string):
        print(session_string)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_session_string': session_string}})
        print(z)

    async def get_session(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_session_string', None)
    
    # api hash
    async def set_hash(self, id, api_hash):
        print(api_hash)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_api_hash': api_hash}})
        print(z)

    async def get_hash(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_api_hash', None)

    
    # api id
    async def set_api(self, id, api_id):
        print(api_id)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_api_id': api_id}})
        print(z)

    async def get_api(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_api_id', None)
    


    async def set_lazy_target_chat_id(self, id, target_chat_id):
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_target_chat_id': target_chat_id}})
        print(z)

    async def get_lazy_target_chat_id(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_target_chat_id', None)
    
    # enable / disable => forward after rename [cmd = enable_newfile / disable_newfile]
    async def set_forward_after_rename(self, id, status):
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'forward_after_rename': status}})
        print(z)

    async def get_forward_after_rename(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('forward_after_rename', None)

db = Database(DB_URL, DB_NAME)
