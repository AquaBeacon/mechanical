# ============================================================
# 親機TX基板 ネットリスト
# SPRESENSE GPIO(相補PWMペア200kHz) -> MIC4427(デュアルドライバ)
#  -> センタタップ昇圧トランス(1:5, プッシュプル) -> 直列同調L -> TD04A
# 同時にトリガ送信: SPRESENSE GPIO -> MAX3485(送信固定) -> テザーTRGペア
# TD04AのC0は要実測 -> L_tune = 1/(w^2*C0)
# ============================================================
from netlist import Circuit
c = Circuit()
c.add("J_MCU","From_SPRESENSE",["PWM_A","PWM_B","TRG_TX","GND","V3V3"],kind="CONN")
c.add("U1","MIC4427",["INA","INB","OUTA","OUTB","VS","GND"],kind="IC")
c.add("T1","XFMR_CT_1to5",["P1","CT","P2","S1","S2"],kind="T")
c.add("L1","L_tune_meas",["1","2"],kind="L")
c.add("J_XD","XDCR_TD04A",["SIG","GND"],kind="CONN")
c.add("TRIG","MAX3485",["RO","REn","DE","DI","VCC","GND","A","B"],kind="IC",nc=["RO"])
c.add("J_PWR","PWR_12V",["+","-"],kind="CONN")
c.add("J_TETH","TetherConn",["TRG_A","TRG_B","SHLD"],kind="CONN")
for k,v in {"R_INA":"100","R_INB":"100","R_DMP":"10","R_TRM":"120"}.items():
    c.add(k,v,["1","2"],kind="R")
for k,v in {"C_VS1":"100n","C_VS2":"10u","C_BULK":"100u","C_T1":"100n","C_TR":"100n"}.items():
    c.add(k,v,["1","2"],kind="C")
c.add("D_SN1","SMBJ33A",["A","K"],kind="D")   # 一次側スナバ/クランプ(要調整)

c.connect("V12",["J_PWR.+","U1.VS","C_VS1.1","C_VS2.1","C_BULK.1","T1.CT","D_SN1.K"])
c.connect("V3T",["J_MCU.V3V3","TRIG.VCC","TRIG.DE","C_TR.1"])
c.connect("GND",["J_PWR.-","U1.GND","C_VS1.2","C_VS2.2","C_BULK.2","J_MCU.GND",
                 "TRIG.GND","TRIG.REn","C_TR.2","J_XD.GND","D_SN1.A","C_T1.2","T1.S2","J_TETH.SHLD"])
c.power(["V12","V3T"]); c.ground(["GND"])

c.connect("PWMA",["J_MCU.PWM_A","R_INA.1"])
c.connect("PWMB",["J_MCU.PWM_B","R_INB.1"])
c.connect("INA",["R_INA.2","U1.INA"])
c.connect("INB",["R_INB.2","U1.INB"])
c.connect("DRV_A",["U1.OUTA","T1.P1"])
c.connect("DRV_B",["U1.OUTB","T1.P2"])
c.connect("SEC_HI",["T1.S1","L1.1"])
c.connect("XD_DRV",["L1.2","R_DMP.1"])
c.connect("XD_SIG",["R_DMP.2","J_XD.SIG","C_T1.1"])
c.connect("TRG_DI",["J_MCU.TRG_TX","TRIG.DI"])
c.connect("TRG_A",["TRIG.A","J_TETH.TRG_A","R_TRM.1"])
c.connect("TRG_B",["TRIG.B","J_TETH.TRG_B","R_TRM.2"])
ok=c.check(); print("ERC:","PASS" if ok else "FAIL")
assert ok
open("tx_pinmap.txt","w").write(c.pinmap()+"\n\n"+c.netlist_table())
print("saved tx_pinmap.txt")
