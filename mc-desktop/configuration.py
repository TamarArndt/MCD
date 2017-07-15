
class Configuration():
    """ sets up paths to .db, .jar und .model files, uses default unless declared otherwise """
    def __init__(self, db_path, jar_path, model_path):
        self.DB_PATH = db_path
        self.JAR_PATH = jar_path
        self.MODEL_PATH = model_path