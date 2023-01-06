from abc import ABC, abstractmethod


class AbstractMobileUIFactory(ABC):
    """
    Class representing app UI and the supported features
    """

    @abstractmethod
    def create_story(self):
        pass

    @abstractmethod
    def upload_photo(self):
        pass


class AndroidFactory(AbstractMobileUIFactory):
    """
    Class for Android related features
    """

    def create_story(self):
        print("Inside AndroidFactory class")
        AndroidCreateStory().story()

    def upload_photo(self):
        print("Inside AndroidFactory class")
        AndroidUploadPhoto().photo()


class IosFactory(AbstractMobileUIFactory):
    """
    Class for iOS related features
    """

    def create_story(self):
        print("Inside IosFactory class")
        IosCreateStory().story()

    def upload_photo(self):
        print("Inside IosFactory class")
        IosUploadPhoto().photo()


class SymbianFactory(AbstractMobileUIFactory):
    """
    Class for Symbian related features
    """

    def create_story(self):
        print("Inside SymbianFactory class")
        SymbianCreateStory().story()

    def upload_photo(self):
        print("Inside SymbianFactory class")
        SymbianUploadPhoto().photo()


class AbstractCreateStory(ABC):
    """
    Class to provide create story feature
    """

    @abstractmethod
    def story(self):
        pass


class AndroidCreateStory(AbstractCreateStory):
    """
    Class to create story on Android platform
    """

    def story(self):
        print("[Android] Creating story on android platform.")


class IosCreateStory(AbstractCreateStory):
    """
    Class to create story on iOS platform
    """

    def story(self):
        print("[IOS] Creating story on IOS platform.")


class SymbianCreateStory(AbstractCreateStory):
    """
    Class to create story on Symbian platform
    """

    def story(self):
        print("[Symbian] Ok boomer! Creating story on Symbian platform, while we can!!")


class AbstractUploadPhoto(ABC):
    """
    Class to provide upload photo feature
    """

    @abstractmethod
    def photo(self):
        pass


class AndroidUploadPhoto(AbstractUploadPhoto):
    """
    Class to upload photo on Android platform
    """

    def photo(self):
        print("[Android] Uploading photo on android platform.")


class IosUploadPhoto(AbstractUploadPhoto):
    """
    Class to upload photo on iOS platform
    """

    def photo(self):
        print("[IOS] Uploading photo on IOS platform.")


class SymbianUploadPhoto(AbstractUploadPhoto):
    """
    Class to upload photo on Symbian platform
    """

    def photo(self):
        print(
            "[Symbian] So you want us to upload petroglyph? Since we are backward compatible, why not! Uploading photo on Symbian platform"
        )


class Application:
    def get_factory(self, platform_type):
        factory = None
        if platform_type == "Android":
            factory = AndroidFactory()
        elif platform_type == "IOS":
            factory = IosFactory()
        elif platform_type == "Symbian":
            factory = SymbianFactory()
        else:
            print("ERROR: unknown platform type.")
        return factory

    def create_story(self, factory=None):
        if not factory:
            print("factory object not passed")
        factory.create_story()

    def upload_photo(self, factory=None):
        if not factory:
            print("factory object not passed")
        factory.upload_photo()


if __name__ == "__main__":
    app_object = Application()

    # in real world scenarios, instead of pass hardcoded platform type we can read platform type from config file.
    print("Running for Android platform...")
    factory_object = app_object.get_factory("Android")
    factory_object.create_story()
    factory_object.upload_photo()
    print("\n")

    print("Running for IOS platform...")
    factory_object = app_object.get_factory("IOS")
    factory_object.create_story()
    factory_object.upload_photo()
    print("\n")

    print("Running for Symbian platform...")
    factory_object = app_object.get_factory("Symbian")
    factory_object.create_story()
    factory_object.upload_photo()
    print("\n")
