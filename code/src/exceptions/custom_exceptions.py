
class BadRegionError(Exception):

    def __init__(self, service_type: str, message: str = 'There is an error in the region'):
        self.service_type = service_type
        self.message = message
        super().__init__(self.message)


class NoServiceTypeError(Exception):

    def __init__(self, message: str = 'There is not a Service Type Name'):
        self.message = message
        super().__init__(self.message)


class NoBucketName(Exception):

    def __init__(self, message: str = 'There is not a bucket name in the S3 call'):
        self.message = message
        super().__init__(self.message)
