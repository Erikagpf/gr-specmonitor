from specmonitor import labeling_framework as lf
from specmonitor import labeling_modules
logger = lf.DynamicLogger(__name__)

class Tx(lf.preRFTask):
    @staticmethod
    def depends_on():
        return 'waveform'

class TxImg(lf.ImgSpectrogramBoundingBoxTask):
    @staticmethod
    def depends_on():
        return 'Tx'

class Waveform32fc(lf.Convert32fcTask):
    @staticmethod
    def depends_on():
        return 'waveform'

class WaveformClean(lf.RemoveIQSamples):
    @staticmethod
    def depends_on():
        return 'waveform'
class TxClean(lf.RemoveIQSamples):
    @staticmethod
    def depends_on():
        return 'Tx'

class AWGNCmdSession(lf.CmdSession):
    pass

if __name__ == "__main__":
    lf.session.run(session=AWGNCmdSession)
