from transstellar.framework.application import Application


class TestApplication:
    def test(self, request, testrun_uid):

        application = Application(request, testrun_uid, {"enable_e2e": True})

        application.close()
