from calc_coeff import *


# Количество дней в рассматриваемой единице времени
t = 1

# Туристские объекты, входящие в ООПТ
tur_objs = []

to_1 = TurObjArea(name='Туристический объект площадной',
                  Cfn=[1, 0.5, 0.89], MC=1, A=110, Au=5, T=18, Td=6, t=t)
tur_objs.append(to_1)

rs_to_2 = [OneDayTouristRouteWithoutTimeLim(DTp=10, DGp=1, Tdp=2, tp=1),
           OneDayTouristRouteWithoutTimeLim(DTp=10, DGp=1, Tdp=2, tp=1)]
to_2 = TurObjWithoutTimeLim(name='Туристический объект с ограничением по времени',
                            Cfn=[0.9, 0.83], MC=1, Ts=16, GS=7, t=t, routes=rs_to_2)
tur_objs.append(to_2)

rs_to_3 = [OneDayTouristRouteWithTimeLim(DGp=5, Tdp=13, tp=1, vp=4)]
to_3 = TurObjWithTimeLim(name='Туристический объект без ограничений по времени',
                         Cfn=[1, 0.5, 0.89], MC=1, Ts=18, GS=5, t=t, routes=rs_to_3)
tur_objs.append(to_3)

rs_to_4 = [OneDayTouristRouteWithTimeLim(DGp=5, Tdp=13, tp=1, vp=4),
           OneDayTouristRouteWithTimeLim(DGp=3, Tdp=12, tp=2, vp=5)]
to_4 = TurObjAutonomous(name='Туристический объект автономный',
                        Cfn=[0.65, 0.99, 0.36], MC=1, Ts=17, GS=15, t=t, routes=rs_to_4)
tur_objs.append(to_4)

# Расчет предельно допустимых рекреационных емкостей туристских объектов, входящих в ООПТ
list_RCCq_tur_obj = []
for tur_obj in tur_objs:
    RCCq = tur_obj.calculate_rccq(tur_obj.calculate_pccq(tur_obj.calculate_bccq()))
    print('-----------------')
    print('Name: ', tur_obj.name)
    print('RCCq: ', RCCq)
    print('-----------------')
    list_RCCq_tur_obj.append(RCCq)

# Расчет предельно допустимой рекреационной емкости ООПТ
RCCoopt = calculate_rccoopt(list_RCCq_tur_obj)
print('Предельно допустимая рекреационная емкость особо охраняемой природной территории: ', RCCoopt)