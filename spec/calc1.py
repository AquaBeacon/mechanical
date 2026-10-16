# AquaBeacon 詳細設計 数値計算（支配式コメント＋assert）
import math

print("="*60); print("A. 音響測距タイミング予算")
# 距離分解能: d = c*dt, dc/dT ~ 2.7 m/s/K (海水20C付近, Medwin近似の傾き)
c = 1500.0            # m/s 公称
d_max = 15.0          # m
t_max = d_max/c
print(f"15m伝搬時間 = {t_max*1e3:.2f} ms")

# RP2040 PIO 分解能: sysclk 125MHz -> 8ns
t_pio = 8e-9
e_pio = c*t_pio
print(f"PIO量子化誤差 = {e_pio*1e3:.3f} mm")
assert e_pio < 1e-3   # 1mm未満

# 水晶 ±30ppm がΔt計測に乗る
e_xtal = 30e-6 * t_max * c
print(f"水晶30ppm誤差@15m = {e_xtal*1e3:.2f} mm")
assert e_xtal < 5e-3

# トリガ線遅延: ケーブル ~5ns/m, RS485送受 ~各100ns(型番要確認)
t_trig = 5e-9*30 + 2*100e-9
print(f"トリガ経路遅延(30m) = {t_trig*1e9:.0f} ns -> 系統誤差 {c*t_trig*1e3:.2f} mm (較正で除去可)")

# 音速の不確かさ: dc/dT ≈ 2.7 m/s/K -> 温度±1Kで
dc_dT = 2.7
for dT in (0.5, 1.0, 3.0):
    e = dc_dT*dT/c * d_max
    print(f"  水温誤差±{dT}K -> 距離誤差 {e*100:.1f} cm @15m")
# 温度センサ必須の根拠。±0.5K計測でcm級を守る
assert dc_dT*0.5/c*d_max < 0.02

print(); print("="*60); print("B. RX利得予算とGBW")
# 受信信号を~1mVpと仮定(要実測)。包絡線検波に~1Vp必要 -> 60dB
v_in = 1e-3; v_det = 1.0
G_total = v_det/v_in
print(f"必要総利得 = {G_total:.0f}倍 ({20*math.log10(G_total):.0f} dB)")
G1, G_bpf, G3 = 20.0, 2.0, 25.0
G_chain = G1*G_bpf*G3
print(f"配分: 初段x{G1} × BPFx{G_bpf} × 後段x{G3} = {G_chain:.0f}倍")
assert G_chain >= G_total

f0 = 200e3
# 非反転段: 閉ループBW ≈ GBW/G。f0の5倍のBW余裕を要求
for name,G in (("初段",G1),("後段",G3)):
    gbw_min = G*f0*5
    print(f"{name} G={G:.0f}: 必要GBW ≥ {gbw_min/1e6:.0f} MHz (候補: OPA607(50MHz)等, データシート要確認)")
# スルーレート: SR ≥ 2πf·Vp, 出力2Vp@200kHz
SR_req = 2*math.pi*f0*2.0
print(f"必要SR ≥ {SR_req/1e6:.1f} V/us")

print(); print("="*60); print("C. MFBバンドパス定数 (C1=C2=C)")
# 支配式: R2=2Q/(w0 C), R1=Q/(H0 w0 C), R3=Q/((2Q^2-H0) w0 C), 条件 2Q^2>H0
def mfb(f0, Q, H0, C):
    w0=2*math.pi*f0
    assert 2*Q*Q > H0, "2Q^2>H0 violated"
    R2=2*Q/(w0*C); R1=Q/(H0*w0*C); R3=Q/((2*Q*Q-H0)*w0*C)
    return R1,R2,R3
for f,C in ((200e3,330e-12),(50e3,1.5e-9)):
    Q,H0=2.5,2.0
    R1,R2,R3=mfb(f,Q,H0,C)
    bw=f/Q
    # MFB必要GBW目安: ≥ 20*Q^2*f0
    gbw=20*Q*Q*f
    print(f"f0={f/1e3:.0f}kHz C={C*1e12:.0f}pF Q={Q} H0={H0}: R1={R1/1e3:.2f}k R2={R2/1e3:.2f}k R3={R3:.0f}Ω BW={bw/1e3:.0f}kHz 必要GBW≥{gbw/1e6:.0f}MHz")
    for R in (R1,R2,R3): assert 100<=R<=1e6, "実装可能な抵抗範囲"

print(); print("="*60); print("D. 包絡線検波RCとエッジウォーク")
# 200kHz搬送(5us周期)。リップル抑制 vs 立上り遅れ
tau=15e-6
ripple=math.exp(-5e-6/tau)   # 1周期での減衰残り
print(f"tau={tau*1e6:.0f}us: 搬送1周期の保持率={ripple*100:.0f}% (リップル小), 包絡線立上り~{2.2*tau*1e6:.0f}us")
# 振幅2倍差での閾値到達時刻差(1次近似): dt = tau*ln(2)
walk=tau*math.log(2)
print(f"振幅2x差のエッジウォーク ≈ {walk*1e6:.1f} us -> {c*walk*100:.1f} cm  ←最重要の系統誤差。距離較正/振幅補正で対処")

print(); print("="*60); print("E. 電力・電池")
# 子機: Pico~0.15W, RXアナログ~0.2W, IMU/RTC~0.05W, ライト6W(絞り運用)
P_elec=0.5; P_light=6.0; hours=3.0
E=(P_elec+P_light)*hours
batt_Wh=11.1*5.0
print(f"子機3h消費={E:.1f}Wh, LiPo3S5000mAh={batt_Wh:.1f}Wh, 余裕率={batt_Wh/E:.2f}")
assert batt_Wh/E > 1.5
# 親機: SPRESENSE+IMU~0.7W, PiZero2W+GSカメラ~2.5W, GPS0.15W, TX平均~0.3W(バースト), RS485 0.1W
P_parent=0.7+2.5+0.15+0.3+0.1
E_p=P_parent*hours
batt_p=11.1*2.2
print(f"親機3h消費={E_p:.1f}Wh, LiPo3S2200mAh={batt_p:.1f}Wh, 余裕率={batt_p/E_p:.2f} ←親機電池がBOM漏れ、追加要")
assert batt_p/E_p > 1.5

print(); print("="*60); print("F. 親機フロート浮力・復原性(概算)")
# 質量見積: 箱+電池+基板1.2kg, フレーム0.6kg, カメラポッド0.5kg, TD04A+ケーブル0.3kg, バラスト0.4kg
m=1.2+0.6+0.5+0.3+0.4
V_req=m/1000.0  # m^3 (淡水)
print(f"総質量~{m:.1f}kg -> 必要排水量{V_req*1e3:.1f}L, 予備浮力50%で{V_req*1.5*1e3:.1f}L")
# 直径30cmリング(断面D=8cm)の排水体積: V= (pi*D^2/4)*(pi*Dring)
Dring=0.30; Dsec=0.08
V_ring=(math.pi*Dsec**2/4)*(math.pi*Dring)
print(f"リング浮子(外径{Dring*100:.0f}cm,断面{Dsec*100:.0f}cm)全没体積={V_ring*1e3:.2f}L")
assert V_ring > V_req  # 半没運用で予備浮力を残す
# 復原性: 重心を下げる(TX/ポッド/バラストが下) -> メタセンタ高GM>0を実測確認とだけ規定

print(); print("="*60); print("G. 子機ステレオ基線")
# sigma_Z = Z^2 * sigma_d / (f_px * B)
W=3840; fov_air=math.radians(120); fov_w=2*math.atan(math.tan(fov_air/2)/1.33)
f_px=W/(2*math.tan(fov_w/2))
print(f"Osmo水中換算FOV~{math.degrees(fov_w):.0f}° -> f≈{f_px:.0f}px")
for B in (0.20,0.30,0.40):
    for Z in (1.0,2.0,5.0):
        sZ=Z*Z*1.0/(f_px*B)
        print(f"  B={B*100:.0f}cm Z={Z}m: 深度分解能≈{sZ*1000:.1f}mm/px視差")
print("-> B=30cmを推奨(2mで~8mm/px)")
