from whitenoise import WhiteNoise


class ESM(WhiteNoise):
    def immutable_file_test(self, path, url):
        return True
