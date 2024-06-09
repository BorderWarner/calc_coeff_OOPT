from typing import List


def calculate_rccoopt(RCCqms: list[int]):
    """
    :param RCCqms: массив предельно допустимых рекреационных емкостей туристских объектов, человек в единицу времени
    :return: Предельно допустимая рекреационная емкость особо охраняемой природной территории
    """
    return sum(RCCqms)


class TurObj:
    def __init__(self, name: str, Cfn: list[float], MC: float):
        """
        Туристический объект
        :param Cfn (list[float]): поправочные коэффициенты, которые учитывают определенные для туристских объектов лимитирующие факторы развития туризма (экологического, социального и социокультурного характера) и установленные режимы использования туристских объектов
        :param MC (float): коэффициент управленческой емкости, долей от единицы
        """
        self.name = name
        self.Cfn = Cfn
        self.MC = MC

    def calculate_pccq(self, BCCq: int):
        """
        :param BCCq: базовая рекреационная емкость туристского объекта, выраженная в целочисленном значении, человек в единицу времени
        :return: Потенциальная рекреационная емкость туристского объекта
        """
        product_Cfn = 1
        for Cf in self.Cfn:
            product_Cfn *= Cf
        return int(BCCq * product_Cfn)

    def calculate_rccq(self, PCCq: int):
        """
        :param PCCq: потенциальная рекреационная емкость туристского объекта, человек в единицу времени
        :return: Предельно допустимая рекреационная емкость туристского объекта
        """
        return int(PCCq * self.MC)


class TurObjArea(TurObj):
    def __init__(self, name, Cfn, MC, A: float, Au: float, T: float, Td: float, t: int):
        """
        :param A: площадь туристского объекта, на которой осуществляется туризм, кв. метров
        :param Au: площадь туристского объекта, необходимая для одного посетителя при осуществлении туризма (кв. метров)
        :param T: количество часов в сутки, когда туристский объект доступен для посещения, часов
        :param Td: среднее время пребывания посетителя на туристском объекте, часов
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        """
        super().__init__(name, Cfn, MC)
        self.A = A
        self.Au = Au
        self.T = T
        self.Td = Td
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        return int((self.A / self.Au) * self.__calculate_rf() * self.t)

    def __calculate_rf(self):
        """
        :return: Коэффициент возвращения
        """
        return self.T / self.Td


class OneDayTouristRouteWithoutTimeLim:
    def __init__(self, DTp: float, DGp: float, Tdp: float, tp: int):
        """
        :param DTp: длина однодневного туристского маршрута или однодневного участка p многодневного туристского маршрута в дневной переход, км
        :param DGp: оптимальное расстояние между группами на участке p туристского маршрута, км
        :param Tdp: среднее время прохождения участка туристского маршрута p с учетом остановок, часов
        :param tp: количество дней пребывания посетителей на туристском маршруте, единиц
        """
        self.DTp = DTp
        self.DGp = DGp
        self.Tdp = Tdp
        self.tp = tp


class TurObjWithoutTimeLim(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithoutTimeLim]):
        """
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        bccq = 0
        for route in self.routes:
            bccq += (route.DTp / route.DGp) * (self.Ts / route.Tdp) * self.GS * (self.t / route.tp)
        return bccq


class OneDayTouristRouteWithTimeLim:
    def __init__(self, DGp: float, Tdp: float, tp: int, vp: float):
        """
        :param DGp: оптимальное расстояние между группами на участке p туристского маршрута, км
        :param Tdp: среднее время прохождения участка туристского маршрута p с учетом остановок, часов
        :param tp: количество дней пребывания посетителей на туристском маршруте, единиц
        :param vp: средняя скорость передвижения по однодневному участку p туристского маршрута с учетом остановок, км в час
        """
        self.DGp = DGp
        self.Tdp = Tdp
        self.tp = tp
        self.vp = vp


class TurObjWithTimeLim(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithTimeLim]):
        """
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость: float
        """
        bccq = 0
        for route in self.routes:
            bccq += (self.__calculate_gp(route.vp, route.Tdp, route.DGp) * self.GS) * (self.t / route.tp)
        return bccq

    def __calculate_gp(self, vp, Tdp, DGp):
        """
        :return: Максимальное количество групп, которые могут пройти в сутки по однодневному участку туристского маршрута до его закрытия или до окончания светового дня, выражается целочисленным значением (единиц)
        """
        return 1 + int(vp * (self.Ts - Tdp) / DGp)


class TurObjAutonomous(TurObj):
    def __init__(self, name, Cfn, MC, Ts: float, GS: int, t: int, routes: List[OneDayTouristRouteWithTimeLim]):
        """
        :param Ts: длина светового дня или количество времени, когда туристский маршрут доступен для посетителей, часов
        :param GS: среднее количество человек в группе (включая сопровождающих), человек
        :param t: количество дней в рассматриваемую единицу времени (месяц, сезон, год и др.), единиц
        :param routes: лист экземпляров однодневных маршрутов/участков
        """
        super().__init__(name, Cfn, MC)
        self.routes = routes
        self.Ts = Ts
        self.GS = GS
        self.t = t

    def __calculate_gp(self, vp, Tdp, DGp):
        """
        :return: Максимальное количество групп, которые могут пройти в сутки по однодневному участку туристского маршрута до его закрытия или до окончания светового дня, выражается целочисленным значением (единиц)
        """
        return 1 + int(vp * (self.Ts - Tdp) / DGp)

    def calculate_bccq(self):
        """
        :return: Базовая рекреационная емкость
        """
        gps = []
        for route in self.routes:
            gps.append(self.__calculate_gp(route.vp, route.Tdp, route.DGp))
        return min(gps) * self.GS * self.t


# Пример расчета предельно допустимой рекреационной емкости особо охраняемой природной территории

# Туристские объекты
tur_objs = []

to_1 = TurObjArea(name='Туристический объект площадной',
                  Cfn=[1, 0.5, 0.89], MC=1, A=110, Au=5, T=18, Td=6, t=7)
tur_objs.append(to_1)

rs_to_2 = [OneDayTouristRouteWithoutTimeLim(DTp=10, DGp=1, Tdp=2, tp=1),
           OneDayTouristRouteWithoutTimeLim(DTp=10, DGp=1, Tdp=2, tp=1)]
to_2 = TurObjWithoutTimeLim(name='Туристический объект с ограничением по времени',
                            Cfn=[0.9, 0.83], MC=1, Ts=16, GS=7, t=7, routes=rs_to_2)
tur_objs.append(to_2)

rs_to_3 = [OneDayTouristRouteWithTimeLim(DGp=5, Tdp=13, tp=1, vp=4)]
to_3 = TurObjWithTimeLim(name='Туристический объект без ограничений по времени',
                         Cfn=[1, 0.5, 0.89], MC=1, Ts=18, GS=5, t=7, routes=rs_to_3)
tur_objs.append(to_3)

rs_to_4 = [OneDayTouristRouteWithTimeLim(DGp=5, Tdp=13, tp=1, vp=4),
           OneDayTouristRouteWithTimeLim(DGp=3, Tdp=12, tp=2, vp=5)]
to_4 = TurObjAutonomous(name='Туристический объект автономный',
                        Cfn=[0.65, 0.99, 0.36], MC=1, Ts=17, GS=15, t=7, routes=rs_to_4)
tur_objs.append(to_4)

# Расчет предельно допустимых рекреационных емкостей туристских объектов
list_RCCq_tur_obj = []
for tur_obj in tur_objs:
    RCCq = tur_obj.calculate_rccq(tur_obj.calculate_pccq(tur_obj.calculate_bccq()))
    print('-----------------')
    print('Name: ', tur_obj.name)
    print('RCCq: ', RCCq)
    print('-----------------')
    list_RCCq_tur_obj.append(RCCq)

RCCoopt = calculate_rccoopt(list_RCCq_tur_obj)
print('Предельно допустимая рекреационная емкость особо охраняемой природной территории: ', RCCoopt)
