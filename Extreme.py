from NKTP_DLL import *

class SuperK:

    def __init__(self, queue, end_flag):
        super(SuperK, self).__init__()
        self.q = queue
        self.end_flag = end_flag

    def rasor_on(self):
        """
        インターロック、エミッションを解除後、総出力10%のパワーモード、シャッターで10%に減衰させた640nmをONにする
        :return: None
        """
        closePorts('COM3')
        self.interlock = registerWriteU16('COM3', 15, 0x32, 1, -1)  # 32 Interlock (>0=reset interlock) U16 1
        self.emission = registerWriteU8('COM3', 15, 0x30, 3, -1)  # 30 Emission 0=Off;3=On U8 1
        print('interlock OFF: ', RegisterResultTypes(self.interlock))
        print('emission ON: ', RegisterResultTypes(self.emission))

        self.mode = registerWriteU16('COM3', 15, 0x31, 1, -1)  # 31 Setup bits 0=Current mode;1=Power mode U16 1
        self.power = registerWriteU16('COM3', 15, 0x37, 100, -1)  # 37 Power level % U16 0.1  powerの初期値は10%
        print('power ON: ', RegisterResultTypes(self.mode))
        print('power ON: ', RegisterResultTypes(self.power))

        self.wave_length = registerWriteU32('COM3', 16, 0x90, 640000, -1)  # 90 Wavelength #0 nm U32 0.001 #初期値640nm
        self.wave_length = registerWriteU16('COM3', 16, 0xB0, 100, -1)  # B0 Amplitude #0 % U16 0.1 #0の初期値は10%

        """ # FSKオプションで使用（買った？買ってればgainができるとか）
        registerWriteU8('COM3', 16, 0x3B, 1, -1)  # 3B FSK mode - U8 1
        registerWriteU8('COM3', 16, 0x3C, 0, -1)  # 3C Daughter board enable/disable dec U8 1
        """

        self.rf_power = registerWriteU8('COM3', 16, 0x30, 1, -1)  # 30 RF Power 0=Off;1=On U8 1
        print('RF power ON: ', RegisterResultTypes(self.rf_power))

    def change_power_value(self, p_value, rasor_no=99):
        """
        出力とレーザー番号を受け取り、装置に渡す
        :param p_value:出力10%～100%
        :param rasor_no: シャッター番号:0～7 総出力：99
        :return: None
        """

        self._p_value = int(p_value * 10)
        if self._p_value >= 1000:
            self._p_value = 1000
        elif self._p_value <= 100:
            self._p_value = 100
        else:
            pass

        if rasor_no == 99:
            self.power_value = registerWriteU16('COM3', 15, 0x37, self._p_value, -1)
        else:
            self.select_no = 176+int(rasor_no)
            self.power_value = registerWriteU16('COM3', 16, self.select_no, self._p_value, -1)
        print('rasor no: ', rasor_no, ' power value %: ', self._p_value/10)

    def change_wave(self, w_length, rasor_no=0):
        """

        :param w_length: 波長:640～900
        :param rasor_no: シャッター番号:0～7
        :return: None
        """
        self.wave = int(w_length * 1000)
        if self.wave >= 900000:
            self.wave = 900000
        elif self.wave <= 640000:
            self.wave = 640000
        else:
            pass
        self.select_no = 144 + int(rasor_no)
        self.wave_length = registerWriteU32('COM3', 16, self.select_no, self.wave, -1)
        print('rasor no: ', rasor_no, ' wave length nm: ', self.wave/1000)


    def rasor_off(self):
        self.close = registerWriteU8('COM3', 15, 0x30, 0, -1)
        self.rf_power = registerWriteU8('COM3', 16, 0x30, 0, -1)
        print('close: ', RegisterResultTypes(self.close))
