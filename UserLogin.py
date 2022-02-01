class UserLogin():
    def initDB(self, id, db):
        self.user = db.query.filter_by(id=id).first()
        print(self.user, 'DB')
        return self

    def created(self, user):
        self.user = user
        print(self.user, 'created')
        return self

    def User(self, user):
        self.user = user
        return self.user

    def is_autorisation(self):
        print('auth')
        return True

    def is_active(self):
        print(self, 'active')
        return True

    def is_anonyme(self):
        print(self, 'anonim')
        return False

    def get_id(self):
        print(self.user.id, 'id')
        return str(self.user.id)

