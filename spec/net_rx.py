# ============================================================
# 子機RX基板 ネットリスト最終版
# XDCR -AC- [clamp,VMIDバイアス] -> 初段非反転x20 -> MFB BPF(f0=200k,Q=2.5,G=2)
#  -> 後段非反転x25 -> AC結合 -> BAT54+RC包絡線 -> TLV3501 -> Pico GP2 (PIO)
# トリガ: MAX3485(受信固定) -> GP6 (PIO)。閾値: GP16 PWM+RC。振幅: 分圧->ADC0
# RP2040ピン多重化: I2C0=GP4/5, SPI1=GP10-13, UART1=GP8/9 (データシート準拠)
# ============================================================
from netlist import Circuit
c = Circuit()
c.add("J_XD","XDCR_TD04A",["SIG","GND"],kind="CONN")
c.add("D_PR","BAV99",["IO","VCC","GND"],kind="D")
c.add("U1","OPA2607_A",["OUT_A","IN-_A","IN+_A","V-","V+"],kind="IC")
c.add("U1B","OPA2607_B",["OUT_B","IN-_B","IN+_B"],kind="IC")
c.add("U2","OPA607",["OUT","IN-","IN+","V-","V+"],kind="IC")
c.add("D_ENV","BAT54",["A","K"],kind="D")
c.add("U3","TLV3501",["OUT","IN-","IN+","V-","V+","SHDN"],kind="IC")
c.add("PICO","RPi_Pico",["GP2","GP3","GP4","GP5","GP6","GP8","GP9","GP10","GP11","GP12","GP13","GP14","GP16","GP17","GP26_ADC0","3V3","VSYS","GND"],kind="IC")
c.add("IMU","BMI270_mod",["SDA","SCL","VDD","GND","INT1"],kind="IC")
c.add("RTC","DS3231_mod",["SDA","SCL","VCC","GND"],kind="IC")
c.add("SD","microSD_SPI",["MISO","MOSI","SCK","CS","VCC","GND"],kind="IC")
c.add("RS485","W_TTL_RS485",["RXD","TXD","RSE","VCC","GND","A","B"],kind="IC")
c.add("TRIG","MAX3485",["RO","REn","DE","DI","VCC","GND","A","B"],kind="IC")
c.add("BUCK","DCDC_5V",["VIN","GND_IN","VOUT","GND_OUT"],kind="IC")
c.add("REG33","AP2112_33",["VIN","GND","EN","NC","VOUT"],kind="IC",nc=["NC"])
c.add("J_BAT","LiPo3S_XT30",["+","-"],kind="CONN")
c.add("F1","FUSE_3A",["1","2"],kind="F")
c.add("SW1","PWR_SW",["1","2"],kind="SW")
c.add("J_TETH","TetherConn",["TRG_A","TRG_B","D_A","D_B","SHLD"],kind="CONN")
for k,v in {"R_G1a":"1k","R_G1b":"19k","R1":"3.01k","R2":"12.06k","R3":"574",
 "R_G3a":"1k","R_G3b":"24k","R_BL":"10k","R_ENV":"10k","R_TH":"10k","R_HYS":"1M",
 "R_DV1":"10k","R_DV2":"10k","R_B1":"100k","R_B2":"100k","R_B3":"100k",
 "R_TRM":"120"}.items(): c.add(k,v,["1","2"],kind="R")
for k,v in {"C_AC1":"100n","C_AC2":"1u","C_AC3":"1u","C_AC4":"100n",
 "C_BPF1":"330p","C_BPF2":"330p","C_ENV":"1n5","C_TH":"100n","C_VM":"10u",
 "C_D1":"100n","C_D2":"100n","C_D3":"100n","C_D4":"100n","C_D5":"100n","C_D6":"100n",
 "C_BK1":"22u","C_BK2":"22u","C_AN":"10u"}.items(): c.add(k,v,["1","2"],kind="C")

# 電源
c.connect("VBAT",["J_BAT.+","F1.1"])
c.connect("VBAT_F",["F1.2","SW1.1"])
c.connect("VBAT_S",["SW1.2","BUCK.VIN","C_BK1.1"])
c.connect("V5",["BUCK.VOUT","PICO.VSYS","RS485.VCC","TRIG.VCC","REG33.VIN","C_BK2.1","C_D5.1"])
c.connect("V3A",["REG33.VOUT","U1.V+","U2.V+","U3.V+","C_AN.1","C_D1.1","C_D2.1","C_D3.1","R_B1.1","D_PR.VCC"])
c.connect("V3D",["PICO.3V3","IMU.VDD","RTC.VCC","SD.VCC","REG33.EN","C_D4.1","C_D6.1"])
c.connect("GND",["J_BAT.-","BUCK.GND_IN","BUCK.GND_OUT","REG33.GND","PICO.GND",
 "U1.V-","U2.V-","U3.V-","IMU.GND","RTC.GND","SD.GND","RS485.GND","TRIG.GND",
 "J_XD.GND","D_PR.GND","R_B2.2","R3.2","C_VM.2","C_AC2.2","C_AC3.2","R_BL.2",
 "C_ENV.2","R_ENV.2","C_TH.2","R_DV2.2","TRIG.DE","TRIG.DI",
 "C_BK1.2","C_BK2.2","C_AN.2","C_D1.2","C_D2.2","C_D3.2","C_D4.2","C_D5.2","C_D6.2",
 "TRIG.REn","J_TETH.SHLD"])
c.power(["VBAT","VBAT_F","VBAT_S","V5","V3A","V3D"]); c.ground(["GND"])

# バイアス&初段
c.connect("VMID",["R_B1.2","R_B2.1","C_VM.1","R_B3.1","U1B.IN+_B"])
c.connect("XD_IN",["J_XD.SIG","C_AC1.1"])
c.connect("ST1_INP",["C_AC1.2","R_B3.2","D_PR.IO","U1.IN+_A"])
c.connect("ST1_FB",["U1.IN-_A","R_G1a.1","R_G1b.1"])
c.connect("ST1_AC",["R_G1a.2","C_AC2.1"])
c.connect("ST1_OUT",["U1.OUT_A","R_G1b.2","R1.1"])
# MFB BPF
c.connect("N1",["R1.2","C_BPF1.1","C_BPF2.1","R3.1"])
c.connect("BPF_OUT",["U1B.OUT_B","C_BPF1.2","R2.1","U2.IN+"])
c.connect("BPF_INN",["U1B.IN-_B","C_BPF2.2","R2.2"])
# 後段
c.connect("ST3_FB",["U2.IN-","R_G3a.1","R_G3b.1"])
c.connect("ST3_AC",["R_G3a.2","C_AC3.1"])
c.connect("ST3_OUT",["U2.OUT","R_G3b.2","C_AC4.1"])
# 検波・比較
c.connect("DET_IN",["C_AC4.2","R_BL.1","D_ENV.A"])
c.connect("ENV",["D_ENV.K","C_ENV.1","R_ENV.1","U3.IN+","R_HYS.1","R_DV1.1"])
c.connect("VTH",["U3.IN-","R_TH.2","C_TH.1"])
c.connect("TH_PWM",["PICO.GP16","R_TH.1"])
c.connect("CMP_OUT",["U3.OUT","PICO.GP2","R_HYS.2"])
c.connect("U3_EN",["U3.SHDN","PICO.GP17"])
c.connect("ENV_ADC",["PICO.GP26_ADC0","R_DV1.2","R_DV2.1"])
# デジタル
c.connect("I2C_SDA",["PICO.GP4","IMU.SDA","RTC.SDA"])
c.connect("I2C_SCL",["PICO.GP5","IMU.SCL","RTC.SCL"])
c.connect("IMU_INT",["PICO.GP3","IMU.INT1"])
c.connect("SPI_CK",["PICO.GP10","SD.SCK"])
c.connect("SPI_TX",["PICO.GP11","SD.MOSI"])
c.connect("SPI_RX",["PICO.GP12","SD.MISO"])
c.connect("SPI_CS",["PICO.GP13","SD.CS"])
c.connect("U1TX",["PICO.GP8","RS485.RXD"])
c.connect("U1RX",["PICO.GP9","RS485.TXD"])
c.connect("485_SE",["PICO.GP14","RS485.RSE"])
c.connect("TRG_RO",["TRIG.RO","PICO.GP6"])
c.connect("TRG_A",["TRIG.A","J_TETH.TRG_A","R_TRM.1"])
c.connect("TRG_B",["TRIG.B","J_TETH.TRG_B","R_TRM.2"])
c.connect("485D_A",["RS485.A","J_TETH.D_A"])
c.connect("485D_B",["RS485.B","J_TETH.D_B"])
ok=c.check(); print("ERC:", "PASS" if ok else "FAIL")
assert ok
open("rx_pinmap.txt","w").write(c.pinmap()+"\n\n"+c.netlist_table())
print("saved rx_pinmap.txt")
