class UserLogin():
    def initDB(self, id, db):
        self.user = db.query.filter_by(id=id).first()

        return self

    def created(self, user):
        self.user = user
        return self

    def User(self, user):
        self.user = user
        return self.user

    def is_autorisation(self):
        return True

    def is_active(self):
        return True

    def is_anonyme(self):
        return False

    def get_id(self):
        print(self.user.id, 'id')
        return str(self.user.id)

