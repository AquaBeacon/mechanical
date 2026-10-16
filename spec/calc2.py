# 実験計画のための追加計算
import math
print("="*60); print("H. バースト長 vs 包絡線検波の応答")
# 包絡線tau=15us。バーストNサイクル(200kHz: 1cyc=5us)後の包絡線到達率 ~ 1-exp(-t/tau)
tau=15e-6
for N in (5,8,10,16,20):
    t=N*5e-6
    frac=1-math.exp(-t/tau)
    print(f"  {N:2d}サイクル({t*1e6:.0f}us): 包絡線がピークの{frac*100:.0f}%まで充電")
# 5サイクルでは81%止まり→閾値マージンが目減り。10サイクル(96%)以上を推奨
assert (1-math.exp(-10*5e-6/tau)) > 0.95

print(); print("="*60); print("I. 期待伝搬時間(プール淡水)")
# 淡水音速 近似: c(T) ≈ 1402.4 + 5.04T - 0.055T^2 + 0.00022T^3 (Marczak近似の丸め,要検証)
def c_fresh(T): return 1402.4 + 5.04*T - 0.055*T*T + 0.00022*T**3
for T in (20,25,28,30):
    print(f"  水温{T}C: c≈{c_fresh(T):.0f} m/s")
T=26.0; c=c_fresh(T)
print(f"  基準 水温26C c={c:.1f} m/s のときの片道伝搬時間:")
for d in (1,5,10,15,20,25):
    print(f"    {d:2d}m: {d/c*1e3:8.3f} ms")
# 1Kあたりの時間変化率→距離誤差(較正の必要性)
dc = c_fresh(27)-c_fresh(26)
print(f"  dc/dT@26C ≈ {dc:.1f} m/s/K -> 25mで {dc/c*25*100:.1f} cm/K")

print(); print("="*60); print("J. 受信振幅のダイナミックレンジ(1m vs 25m)")
# 球面拡散 20log10(r2/r1)。吸収は淡水200kHzで~数dB/km→25mで<0.2dB無視
spread = 20*math.log10(25/1)
print(f"  拡散損失差(1m->25m) = {spread:.1f} dB (≈{10**(spread/20):.0f}倍)")
# 固定利得60dBでは近距離で飽和リスク → 入力減衰ジャンパ(-20dB)を用意
att = 20.0
print(f"  対策: 初段入力に-{att:.0f}dBジャンパ(1k:9k分圧等) -> 近距離試験時のみ挿入")
# 3.3V単電源での飽和判定: 包絡線ADCフルスケール3.3V, 分圧1/2 -> 実効6.6Vppまで観測可
print("  包絡線ADC(1/2分圧)の観測上限: 包絡線3.3*2=6.6V相当…アンプ出力は3.3V電源で飽和が先")
print("  -> 『ADC値が2.9V超=飽和気味』をログ上のフラグ条件とする")

print(); print("="*60); print("K. TX熱・電流の目安(ベンチ試験の合否線)")
# デューティ: 10cyc=50us, 5Hz -> 0.025% 平均は極小。ピーク電流がMIC4427定格1.5A以内か
duty = 50e-6*5
print(f"  duty = {duty*100:.4f} % -> 平均電力は極小、発熱は主に待機損とトランス")
# 12V直駆時のTD04Aピーク電流(C0=2nF仮): I=V*w*C = 12*2pi*200k*2n
I_pk = 12*2*math.pi*200e3*2e-9
print(f"  12V直駆・C0=2nF仮定のピーク容量性電流 ≈ {I_pk*1e3:.0f} mA (MIC4427定格1.5A内)")
assert I_pk < 1.5
print("  合否線: 15分連続で ケースΔT<20K, 12V平均電流<100mA, 波形振幅変動<±10%")

print(); print("="*60); print("L. 統計に必要なピング数")
# 標準偏差の推定: N=30でsigmaの95%CI幅~±25%。各距離30ピング以上を規定
for N in (5,10,30,100):
    ci = 1.96/math.sqrt(2*(N-1))
    print(f"  N={N:3d}: sigma推定の相対95%CI ≈ ±{ci*100:.0f}%")
print("  -> 各距離N≥30(送信5連×6セット以上)を規定。ドラフトの5回では不足")

print(); print("="*60); print("M. マルチパス(プール)の到達時間差")
# 25mプール: 水面反射経路。深さh=1mに送受を置くと反射経路長=2*sqrt((d/2)^2+h^2)*... 鏡像法
h=1.0
for d in (5,10,25):
    direct=d
    refl=2*math.hypot(d/2,h)   # 水面(または底)1回反射の鏡像
    dt=(refl-direct)/c*1e6
    print(f"  d={d:2d}m, 深さ{h}m: 反射経路差={refl-direct:.2f}m -> 遅れ{dt:.0f}us")
print("  -> 直接波の初エッジ検出なら分離可能(遅れ>>バースト50us)だが、")
print("     d=25mでは差53cm/遅れ360usなので、検出ウィンドウを初エッジ後200usで閉じる")
